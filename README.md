# kivy-Interrogazioni

## Data structure

Define lists container
```json
{
    "lists": {
```

Define list name
```json
    "Subject": {
```

Define the days that will be filled and how many peoples to insert each day
```json
        "days":{
            "1/12": 3,
            "2/12": 2,
            "3/12": 3
        }
```

Define the students preferences
```json
        "days_vol": {
            "1/12": ["Andrea", "Cristiano"],
            "2/12": ["Diego"],
            "3/12": ["Erica", "Barbara"]
        },
```

Define a final list of volunteers
```json
        "list": {
            "1/12": ["Andrea", "Cristiano"],
            "2/12": ["Diego"],
            "3/12": ["Erica", "Barbara"]
        }
    }
```

Define all students name after lists definition
```json
    "vol": ["Andrea", "Barbara", "Cristiano", "Diego", "Erica"]
}
```


>## Example
>
>```json
>{
>    "lists": {
>        "Subject": {
>            "days": {
>                "1/12": 3,
>               "2/12": 2,
>                "3/12": 3
>            },
>            "days_vol": {
>                "1/12": ["Andrea", "Cristiano"],
>                "2/12": ["Diego"],
>                "3/12": ["Erica", "Barbara"]
>            },
>            "list": {
>                "1/12": ["Andrea", "Cristiano"],
>                "2/12": ["Diego"],
>                "3/12": ["Erica", "Barbara"]
>            }
>        }
>    },
>    "vol": ["Andrea", "Barbara", "Cristiano", "Diego", "Erica"]
>}
>```
