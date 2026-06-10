# Civil service data utilities

Shared data utilities for civil service data pipelines.

## Related repositories

- 🔓 [Civil service organisations](https://github.com/instituteforgov/cs_organisations/): Scripts for managing canonical civil service organisation data
- 🔓 [Civil service staff numbers](https://github.com/instituteforgov/cs_staff_numbers/): Scripts for extracting civil service staff numbers data
- 🔓 [CSPS extraction](https://github.com/instituteforgov/csps_extraction/): Scripts for extracting Civil Service People Survey data

## Project structure

```
├── cs_data_utils/
│   └── utils.py
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
├── pyproject.toml
└── requirements.txt
```

## Installation

### Installing from GitHub

```bash
pip install git+https://github.com/instituteforgov/cs_data_utils.git@<commit>
```

### Installing as a local package

```bash
pip install -e "<path_to_your_local_copy>/cs_data_utils"
```

NB: Even when installed in this way, in `requirements.txt` this will show a GitHub URL rather than a local path.

## Dependencies

```bash
pip install -r requirements.txt
```

## Contributing

This project uses `pre-commit` hooks to ensure code quality. To set up:

1. Install `pre-commit` on your system if you don't already have it:

    ```bash
    pip install pre-commit
    ```

1. Set up `pre-commit` in your copy of this project. In the project directory, run:

    ```bash
    pre-commit install
    ```

Rules that are applied can be found in [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

The hooks run automatically on commit, or manually with `pre-commit run --all-files`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
