from tqdm import tqdm

from .queries import create_query, QueryFailedError
from .verbal import validate_story, load_story


class QGenerator:
    def __init__(self, builder, transformation, queries, spec_limit=None,
                 model_meta_list=None, graph_cap=None,
                 include_background=False, include_reasoning=True,
                 seed=None, model_kwargs=None, skip_det=False):
        self.builder = builder
        self.transformation = transformation
        self.spec_limit = spec_limit or 1
        self.model_meta_list = model_meta_list
        self.graph_cap = graph_cap
        self.include_background = include_background
        self.include_reasoning = include_reasoning
        self.seed = seed or 69
        self.model_kwargs = model_kwargs or {}
        self.skip_det = skip_det

        if not isinstance(queries, (list, tuple)):
            queries = [queries]
        self.queries = queries

    def get_graphs(self, story):
        graphs = story.get('phenomenon', [])
        if isinstance(graphs, str):
            graphs = [graphs]
        if self.graph_cap is not None:
            graphs = graphs[:self.graph_cap]
        return graphs

    def get_queries(self, story):
        if len(self.queries) > 0:
            return self.queries

        if 'queries' not in story or len(story['queries']) == 0:
            raise ValueError(f'"queries" missing in {story}')
        return [create_query(q) for q in story['queries']]

    def transform(self, labels):
        if self.transformation is not None:
            labels = self.transformation.transform(labels)
        return labels

    def generate_questions(self, story_id):
        story = load_story(story_id)

        if 'scm' not in story:
            raise ValueError(f'"scm" missing in {story}')

        queries = self.get_queries(story)
        # print(queries)
        # print(f'Generating questions for story: {story_id} (queries: {", ".join(q.query_name for q in queries)})')

        graphs = self.get_graphs(story)

        for graph_id in graphs:
            if self.skip_det and graph_id.startswith('det'):
                print(f'Skipped deterministic story: {story_id}')
                return

            story['phenomenon'] = graph_id

            count = self.spec_limit

            if self.builder.is_deterministic:
                count = min(count, self.builder.spec_count(story))

            labels = validate_story(story.copy())

            labels = self.transform(labels)
            failures = {}
            itr = enumerate(self.builder.sample_specs(story, count))
            itr = tqdm(itr, total=count,
                       desc=f'iterating specs for {story_id} ({graph_id})')  # Iterating through distinct graph specifications
            for spec_id, spec in itr:

                model = self.builder.generate_scm(story, spec, seed=self.seed, **self.model_kwargs)

                model_meta = {
                    'story_id': story_id,
                    'graph_id': graph_id,
                    'spec_id': spec_id,
                    'spec': spec,
                    'seed': self.seed,
                    'builder': getattr(self.builder, 'name', None),
                    **self.builder.meta_data(model, labels, spec),
                    **labels.get('meta', {}),
                    'equation_type': getattr(model, 'equation_type', None),
                    'background': model.verbalize_background(labels),
                    'variable_mapping': model.variable_mapping(labels),
                    'structure': model.symbolic_graph_structure(),
                    'params': {str(v): v.param.tolist() for v in model.variables()},
                    **self.model_kwargs
                }

                model_id = len(self.model_meta_list) if self.model_meta_list is not None else None
                if self.model_meta_list is not None:
                    model_meta['groundtruth'] = {
                        'ATE(Y | X)': model.ate('X')['Y'],
                        'ETT(Y | X)': model.ett('X')['Y'],
                        'NDE(Y | X)': model.nde('X', 'Y')['Y'],
                        'NIE(Y | X)': model.nie('X', 'Y')['Y'],
                        'P(Y=1 | X=1)': model.marginals(X=1)['Y'],
                        'P(Y=1 | X=0)': model.marginals(X=0)['Y'],
                        **{f'P({k}=1)': v for k, v in model.marginals().items()}
                    }
                    model_meta = {'model_id': model_id, **model_meta}
                    self.model_meta_list.append(model_meta)

                for query in queries:
                    try:
                        for question_id, entry in enumerate(query.generate_questions(model, labels)):
                            if 'meta' not in entry:
                                entry['meta'] = {}
                            if self.model_meta_list is None:
                                entry['meta']['model'] = model_meta
                            else:
                                entry['meta']['model_id'] = model_id
                                if self.include_background:
                                    entry = {'background': model_meta['background'], **entry}

                            if self.include_reasoning:
                                entry['reasoning'] = query.reasoning(model, labels, entry)

                            entry['meta'] = {
                                'story_id': story_id,
                                'graph_id': graph_id,
                                **entry.get('meta', {})
                            }

                            yield {'desc_id': f'{story_id}-{graph_id}-{query.name}-'
                                              f'model{model_id}-spec{spec_id}-q{question_id}',
                                   **entry}

                    except QueryFailedError as e:
                        if query not in failures:
                            failures[query] = (query, e)

            itr.close()
            if len(failures) > 0:
                print('\n'.join(f'Query {query.name!r} failed for {graph_id!r} (story {story_id!r}): {e}'
                                for query, e in failures.values()))
