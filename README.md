# heat-migration-template-generator
This script was written to help generate heat templates to do blue-green updates on stacks.


# how to use
```
    self.generator = migrationTemplateGenerator('./tests/files/test_v1.yaml', './tests/files/test_v2.yaml')
    generated = self.generator.generateAll()
```
generated will contain 3 templates.

