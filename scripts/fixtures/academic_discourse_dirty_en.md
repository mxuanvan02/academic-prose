# Results

The automatically assigned labels have not been independently validated, and their reliability has not been quantified. Near-duplicate records have not been assessed; therefore, the results do not establish label validity and only describe the current evaluation conditions.

The results only describe performance under oracle context. They do not establish retrieval effectiveness. They cannot guarantee generalization to a deployed system.

# Future research

Future research should validate the labels, must assess near-duplicate records, and needs to report cluster-aware uncertainty.

# Methods

Oracle context isolates answer generation from retrieval, but it does not reproduce operational retrieval because the relevant context is supplied in advance, while Bloom labels are assigned automatically, so the results only characterize the specified conditions, cannot be generalized to deployment, and do not establish label reliability; moreover, the evaluation uses one fixed prompt, one deterministic decoding configuration, and one answer format, although these choices may interact with model behavior, therefore the paragraph obscures several independent claims inside one sentence.
