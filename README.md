# markdown-table-generator


## CLI

```bash
usage: gen_table.py [-h] CONFIG_FILE

Script for creating markdown tables using json config

positional arguments:
  CONFIG_FILE  json file with the configuration

optional arguments:
  -h, --help   show this help message and exit

```

## Examples

**Config file**:
```json
{
    "columns": {
        "Data in the column 1": {
            "label": "1",
            "align": "right",
            "max_len": 15
        },
        "Data in the column 2": {
            "label": "2",
            "align": "left",
            "max_len": 10
        }
    },
    "order": ["2", "1"],
    "rows": [
        {
            "1": "data for column 1",
            "2": "data for column 2"
        },
        {
            "1": "next row",
            "2": "next row"
        },
        {
            "2": "will use empty values for unmentioned keys"
        }
    ]
}
```

**Script result**:
```bash
> $ python gen_table.py config.json 
| Data in<br />the column<br />2 | Data in the<br />column 1 |
| :--- | ---: |
| data for<br />column 2 | data for column<br />1 |
| next row | next row |
| will use<br />empty<br />values for<br />unmentione<br />d keys |  |
```

Its table markdown:

| Data in<br />the column<br />2 | Data in the<br />column 1 |
| :--- | ---: |
| data for<br />column 2 | data for column<br />1 |
| next row | next row |
| will use<br />empty<br />values for<br />unmentione<br />d keys |  |




