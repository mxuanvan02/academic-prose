# Results

Under oracle context, the model answers from a source passage supplied in advance. This design isolates answer generation from retrieval error; the results therefore characterize answer generation when the relevant context is known.

# Limitations

Bloom labels are assigned automatically without expert reference annotations. Analyses by cognitive level consequently treat these labels as operational variables and do not estimate classification reliability.

# Future research

A stratified validation study with multiple experts could estimate label agreement. This evidence would show whether comparisons across Bloom levels remain stable when automatic labels are replaced with reference annotations.

# Methods

The pipeline contains three stages: context extraction, question generation, and candidate filtering. Each stage produces a distinct output, allowing data loss to be localized.
