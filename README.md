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
            "max_len": 10
        },
        "Data in the column 2": {
            "label": "2",
            "align": "left",
            "max_len": 4
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
        }
    ]
}
```

**Script result**:
```bash
> $ python gen_table.py config.json 
| Data<br />in<br />the<br />colu<br />mn 2 | Data in<br />the column<br />1 |
| :--- | ---: |
| data<br />for<br />colu<br />mn 2 | data for<br />column 1 |
| next<br />row | next row |
```

Its table markdown:

| Data<br />in<br />the<br />colu<br />mn 2 | Data in<br />the column<br />1 |
| :--- | ---: |
| data<br />for<br />colu<br />mn 2 | data for<br />column 1 |
| next<br />row | next row |


