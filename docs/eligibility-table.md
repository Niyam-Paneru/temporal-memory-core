# Memory eligibility table

| Known by query time? | Valid at world time? | Allowed use? | Active? | Eligible? |
|---:|---:|---:|---:|---:|
| no | any | any | any | no |
| yes | no | any | any | no |
| yes | yes | no | any | no |
| yes | yes | yes | no | no |
| yes | yes | yes | yes | yes |

After this table passes, eligible supersession is applied. Only then does relevance ranking run.

A highly relevant row cannot “score its way back in” after failing eligibility.
