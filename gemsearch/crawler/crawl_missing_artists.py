from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.storage.Storage import Storage
from gemsearch.crawler.spotify_api import crawlArtist, getSpotipyInstance

missingIds = ["spotify:artist:5Qq4eSnLRNtEjXdFmiP6ei",
"spotify:artist:6C3ZGU59R9XhxQ1KRU5Q1O",
"spotify:artist:5RNnFkux71dFml5xQFOZpJ",
"spotify:artist:2T9xH19b4sNPqfwjPGzejt",
"spotify:artist:7qAWGH2Lb2uIXlZI36YRiO",
"spotify:artist:7km35sbsvoVtpiXtx5pGoS",
"spotify:artist:0pQaD3TPmBbvnNtkLjI0rk",
"spotify:artist:5JC4hm3RYhFmaDsszThQ0K",
"spotify:artist:4L5mYWvi53PhBsE79BBBwj",
"spotify:artist:2X7m5Insddc58AhJTs9t4Q",
"spotify:artist:79aMFcvOfHdzNIXUE5deJb",
"spotify:artist:0tMrilqtMAsG8qWMBvE0F3",
"spotify:artist:3XnXZHeCvofk8ls3v1OsLt",
"spotify:artist:4vkp0Xrh0KIQ5f9D5IlMDm",
"spotify:artist:2jK4QCcb4yhupzNhul3OBn",
"spotify:artist:6OvobXDxB51VcJrrvJ70uq",
"spotify:artist:5ICXL8q6E6KDQg4L2sF7lB",
"spotify:artist:5dYqPL5jCDCO8uIqJKfnex",
"spotify:artist:1jVuLlkfKibBT0hXDnzQjp",
"spotify:artist:0kH3qHYdrKMy2LWAYSZOtz",
"spotify:artist:26mEFuf39TjJAmGWSghqll",
"spotify:artist:6RCjV99oEaLRFDU9KMTdU7",
"spotify:artist:7edwIsK9dqLoNK4RYVJgJx",
"spotify:artist:2UpdDXgm3WrKsw5vvq6EDr",
"spotify:artist:1K4v4BX6X00ICwIAx5VctJ",
"spotify:artist:5YtIFaOP7teAaxzR7lFM8C",
"spotify:artist:3A2zqCB7ygfit7Qi9pT4gT",
"spotify:artist:6hQJolYGOSB4FMc3efwGFF",
"spotify:artist:4K83xBSPCG1yRdbL9KtAex",
"spotify:artist:1UEcsykc01ZacTBAzknW0F",
"spotify:artist:5EgHxnLSdBst14bCceq7S4",
"spotify:artist:5D1OMxu9kunRUiOpqdGT09",
"spotify:artist:5Epr1ym6goZ8c5fqrtysVO",
"spotify:artist:2pO0cSgOsR8aOZL2qVahyC",
"spotify:artist:00IHrMxae2jSiC0oie2iOt",
"spotify:artist:6aHztHryq1gSuO19l8h4Wd",
"spotify:artist:3YL1unICPATKMfWO3MHmLM",
"spotify:artist:5TBVmPKtXOVOs5pQPoaEFU",
"spotify:artist:0szo06FgZwtdDwKjjlJvr2",
"spotify:artist:05HeX90zX2jMoL4mOPBK5v",
"spotify:artist:6PWuHEf0NiiABne867uwpT",
"spotify:artist:66n66O8eyqmQ8uMNarbsaP",
"spotify:artist:3nNOwJqSQSqVbX2nDPZuQ3",
"spotify:artist:1VlUwf7Tvky6oaW3usJkmk",
"spotify:artist:3TzK9tbkliyZcuEAZLFnUu",
"spotify:artist:78n6UEk9sXZhISJxxLPqBU",
"spotify:artist:2tJ6csNN21bhubevSjTfjS",
"spotify:artist:1cBBAsEcsK8lkyiF35nazI",
"spotify:artist:0RFZ7D798BlPzEw0rIrfZy",
"spotify:artist:5j0Mz5zHobfxxxkMB494RH",
"spotify:artist:7JQKCnl4IaJz7uMtcLScfK",
"spotify:artist:32kH7nXJcwt9ZxpMujcu6X",
"spotify:artist:3G7AATlA2J4RXnCE7jhHpJ",
"spotify:artist:5VoLTFWdFjUdf7TfQhD9Kn",
"spotify:artist:3a5tXu7GjZwgRxdzFHuGwg",
"spotify:artist:7D4sK5qupQyzxe7OOkBSyP",
"spotify:artist:6RXH0GYEEitcThocKF6ubE",
"spotify:artist:7FflINZ3oWG2LV1ralZvyq",
"spotify:artist:5amSTggUSnPe1zxKoPLbpN",
"spotify:artist:6AbxjQMrlxoh0C3QLalyl0",
"spotify:artist:5hDZFm1sF9ZiuchgjhzAuN",
"spotify:artist:6USW4Aow7WM7nv5SwuR6WW",
"spotify:artist:6i4JJGr2TG959WrIJxrtHm",
"spotify:artist:0RD0IdS74Qa25dkGJr3qbf",
"spotify:artist:2zZjUO4zxJi9R8V5TR8wsJ",
"spotify:artist:4R1VLKASeLLo3Sxffg3bgU",
"spotify:artist:6lYbkNgJMuhNHLlnQIkWYO",
"spotify:artist:10PhZyEEAFRWaFiX1XFCfg",
"spotify:artist:6RYQixf0tg4yFjXL1swE9A",
"spotify:artist:5Rowuc5XCQz7E8SaOFSue9",
"spotify:artist:1lnBQDbh6lqqlAzWwf9TEQ",
"spotify:artist:3tSeuQkDYNY83Kd3F8FRY4",
"spotify:artist:4zhOboqujLR3HqlcUl9OjG",
"spotify:artist:1ygnFQb0wvgWFS4P020EaY",
"spotify:artist:0wcwd9rVgYgvbSBOlxZRc9",
"spotify:artist:5P3HRFj3CA7VwMDwNLEoBW",
"spotify:artist:6PdAWiOAoN907WFd8Lvn1f",
"spotify:artist:0N0szCLTbptgBsihtgrVMm",
"spotify:artist:6SAKydkM7CGK9gcoRgwvVV",
"spotify:artist:3DkcSJdduzdu3ad3pacv6y",
"spotify:artist:4wcxojDGSFEicXnyDL2iaj",
"spotify:artist:1MnMEVLHbRkl1uGlSKlyId",
"spotify:artist:7aqbqPKSd1TOEdLVFbfhzq",
"spotify:artist:5gmM9QlsqaZGHTP1DajAmG",
"spotify:artist:4ZBRxxqX0tAp4F0TI7ZUhM",
"spotify:artist:1q0Xv4QfM9LpB6rGcMaoZp",
"spotify:artist:2ej8g2yeZxJCPjeo932J5N",
"spotify:artist:3GnSSSD7WTZSyCH8gB8C7z",
"spotify:artist:5Msue2sYv5yczzqvcMMauk",
"spotify:artist:56lzwBqcyHNG4TNOEjZV93",
"spotify:artist:3lzKClB7HjZVwB0k0YjH9U",
"spotify:artist:3josHa5lKmv8GAObuaGCru",
"spotify:artist:1tWVQz2gyHqyxoHhDySdPJ",
"spotify:artist:1ynVm7KApUWdHDW5950Dk4",
"spotify:artist:0faKlLECzDxSOns5J3faZq",
"spotify:artist:0vIWZjyjgs2yAiRNZaijZY",
"spotify:artist:1EbEkOkVXyqtMKt19hoAaS",
"spotify:artist:2kVTq4AEmcrraVsAfOAfd6",
"spotify:artist:3Fe17vEi4rIlhVVclg4MJr",
"spotify:artist:4tFIZqub7GyuKjhWJSYVYs",
"spotify:artist:1w8oGK1cWxlBxy6EhZ04MQ",
"spotify:artist:78IQkRi4w6rehceXlG7Z99",
"spotify:artist:6TkJ1wmZuJbvsU1qJpD0Rg",
"spotify:artist:40fsQ3fhJL3NBRjtqf6QgD",
"spotify:artist:0VpfMl3g232sUSIS7uGeYJ",
"spotify:artist:2ooBJHv2bqaNnHy3xOvBN1",
"spotify:artist:4EvCfYBatA3qLhoIoVkZra",
"spotify:artist:5bt7vHo0Q7dfHlGFfP2ieC",
"spotify:artist:35mdRDPA1ONJfxJCKw4Xnq",
"spotify:artist:1vPVM560hAW5WUmxRQgi3j",
"spotify:artist:0AqIvNyl0pnjdgA0xsMoej",
"spotify:artist:10pF3gZjBdQ2oBkwY7kW8R",
"spotify:artist:5cWhKiS1yW9iH9GirvKXZr",
"spotify:artist:4kJ3SXAmH8Hx9U4DCcVnAH",
"spotify:artist:3EwEPyeCmY05Q3zBcjGxrF",
"spotify:artist:4JyFAZO7QRlFPkqiaQrwGp",
"spotify:artist:5SI9cSi1tWCRBtIBso3MPa",
"spotify:artist:5vFeLkVqyS0PhTsC0Kmeom",
"spotify:artist:0dkrMXbCDBQWABLqBYaeGi",
"spotify:artist:0EARkJQiXURWnxdsXpUEdB",
"spotify:artist:2pSnbGY4UbzdwcXEYKrbvh",
"spotify:artist:0sVImPH0XV2tfaYw3P85pw",
"spotify:artist:56RWGu1VIJgMb4NuB8Ki4A",
"spotify:artist:1e0kruQzIE9vtWIQkyg8pl",
"spotify:artist:6LSxTGTizzIMOJ8x2JK9xR",
"spotify:artist:0dUoqv911AuHP1IsxSsb0m",
"spotify:artist:3Ico8FgtxB4Tog6klZcUqN",
"spotify:artist:1Pg0glqj0nZMrKVNei0F4w",
"spotify:artist:3EsmX7mFCvtOD4NDz31lO7",
"spotify:artist:4hDJQRSI84oHJZmMmEUyqr",
"spotify:artist:206MsX15itIgFVZgOkNjNK",
"spotify:artist:6P62kFLJga5K8VZgwPgHjp",
"spotify:artist:7nQvs6VjFqxMMIHE9IwHo0",
"spotify:artist:6plzDpFbgL6vo5KyRF3wVQ",
"spotify:artist:4SfsNFUMYgONrkNnGNAOyS",
"spotify:artist:4AnPXzLvNImRDVH7taSIKh",
"spotify:artist:0TaDvdzwJjKp98IPCexwi2",
"spotify:artist:1KF2QrohqsmHAUaYBRpceU",
"spotify:artist:2Iqn8dbh4BvojpUyzWYnHg",
"spotify:artist:2ljbmaCLbwDOijSk47cVIy",
"spotify:artist:3sv3aG8UsVHW6yjM33RxVB",
"spotify:artist:7mkJawcqAfz704eTqiKpHA",
"spotify:artist:5a9047zZrZtU89jdo5y6C2",
"spotify:artist:2ZHMCqGdqW9wIhUT23JcwF",
"spotify:artist:2wN2QQ2YECgtsigIUi0eE1",
"spotify:artist:6NQRKlefOLtxziaa7C7TQV",
"spotify:artist:4BuLBR5BjLghO9DeAs2E60",
"spotify:artist:6EsxIgZ40VE33OmowdjOhS",
"spotify:artist:2blTiukutePTy0b54DG2yM",
"spotify:artist:0xLySkunmw0oDbd3fatBJR",
"spotify:artist:0J6bmy3oHmAvm7dgsz9ybD",
"spotify:artist:34X1r749egpzRB7bvawDHa",
"spotify:artist:2nnnioQLeXPCv3Q10hTQJt",
"spotify:artist:7fSvuaDqDF1GksXqliGyPM",
"spotify:artist:11YsAQgccGScEAZrOeV39d",
"spotify:artist:4wwVkh6bosdtbn3pMAtIzG",
"spotify:artist:6ToDkdmL8c1vhsFSl3flRs",
"spotify:artist:5PLSrqlVNdDhSR6VcIbONZ",
"spotify:artist:7rNUiNj0VmiC1Scp2yT1NL",
"spotify:artist:4g6f4USwyc2cDAzNji4lxA",
"spotify:artist:7k2E6cTiLYU3jixudOzenJ",
"spotify:artist:6GLIaTY7TuLggtHLheMo4v",
"spotify:artist:4xvKS93OKYe8elEHHgEpvY",
"spotify:artist:6kkz5CDEAzbOiMBtrrg8YA",
"spotify:artist:0gdXB4hI6K0vmgCby9iIlh",
"spotify:artist:0s1HXWjS0nti6HnuFfOJrT",
"spotify:artist:1LWQhhpQjclzVZ8QZUx9MZ",
"spotify:artist:4NWGsa4ZVst0VeJOvbxLp1",
"spotify:artist:5rYTOrkZ4ZDeDl5oivW4L0",
"spotify:artist:0CcfdbjuPvZ6vvIWgACkhl",
"spotify:artist:41JpE2y2QtxsrZIitf9EPK",
"spotify:artist:2YgTJGfaZQQRq2SKayqOsa",
"spotify:artist:7N2M52V5WDRUsU99SQnj8S",
"spotify:artist:5QUqBvjuXzmYEUbBcX8KxR",
"spotify:artist:2IgYtkgYVCTF2mWKxotLZ5",
"spotify:artist:4a1jYIK2RWOWJJAe6oRTuO",
"spotify:artist:2h1qP1QHYsU7HuizeS23Q4",
"spotify:artist:1X8RgTdpMM8Uj1Q81LXrMB",
"spotify:artist:0GOKSaBWNSG8GIavilb6ph",
"spotify:artist:7lLhP5SNk3pvvHPwdIbn1U",
"spotify:artist:0PUnGhRO8hFBiw6U9BP58u",
"spotify:artist:54eH0dayw2637hB1jBJYJH",
"spotify:artist:6Fvg0pmexrSkR9CVpv43Zt",
"spotify:artist:5fwJTOAbq96KhrQPkUL3No",
"spotify:artist:2J7WVHE3otcfK6kCP6b7Aj",
"spotify:artist:26suYo4HQ2CdqVoTXuKQnj",
"spotify:artist:1GvrYa8T4wZbpfPRbNvn81",
"spotify:artist:46d9KMrs3OE8OZdcPFXZn4",
"spotify:artist:01sOsLYP8axGqCIxX8qKbV",
"spotify:artist:5Rj5SliJYUI7aakR3svIZN",
"spotify:artist:5lyicPWgjd4qlvVsD69F1v",
"spotify:artist:0iNAKSmI4DoB7cnrGxvJq0",
"spotify:artist:4BPQ8agSbp5f64GWn5MsIh",
"spotify:artist:6olxBgfqA9dNDWQzJ2DPy2",
"spotify:artist:4wEoqKZDHBHwOa85iEtJGd",
"spotify:artist:0Yf6vte0XvJ4uguJrO4rj4",
"spotify:artist:2fQ9QcmzRCyJN9E0nk7vdo",
"spotify:artist:5DjpC4cUIWtS8SPR2bafCC",
"spotify:artist:4DZfOyxlorSqIAohFGAYHL",
"spotify:artist:3gTp3IdZbBR0mPA2CbDTXQ",
"spotify:artist:5X3es3V4GHByWBTvOigijp",
"spotify:artist:7mxBsigBiwAQ4AHyi1wVNL",
"spotify:artist:2A8ofpwzI2Y77m0F3U3IlR",
"spotify:artist:6X00fNAOqTGS4cWij2nMOf",
"spotify:artist:4otGYdsNlqUd9cnEfVVD84",
"spotify:artist:3VZYSdTv6izUgirgXLJTbO",
"spotify:artist:00uW4qIzIJ9K7hPZsWUgEz",
"spotify:artist:198VoDWNaRg0lQikp3Vr0T",
"spotify:artist:0t6eSHxuqkOY6I7Y1Zy8zP",
"spotify:artist:0wqCLKcVUa1UCU5yvULmLL",
"spotify:artist:0Va70G0IR4lhBkJcvjlXBA",
"spotify:artist:5JxNJ9e7ybZH9L6y7W8ZQo",
"spotify:artist:2X4t05IDNkrBM7UBM6UwUw",
"spotify:artist:5yuUPUZ9wD73mXQJsPV006",
"spotify:artist:0A6QeGMhNxX3uAXzvVXtYE",
"spotify:artist:1VnhAAvyGhV8YTISxbSFI4",
"spotify:artist:7z1FpVWm4XjH5tWtbgU7RR",
"spotify:artist:2uNAb8UDCY2jV0nCJVZN1j",
"spotify:artist:2hihHHuMZqzvHSClXzm6bX",
"spotify:artist:5txtgUrxp6rVhDaZq0U59F",
"spotify:artist:69gCUdx5uGCN4cTgSq4Cd6",
"spotify:artist:706HefPGK6rrXNnxBMPncu",
"spotify:artist:78dVkWXzW1iiPDTEAhaUVM",
"spotify:artist:25tgGtNqDW1omxhzGMbpcw",
"spotify:artist:2dy6tyQjm88QzBshPmkran",
"spotify:artist:1Kx8RRb1Tsj8izLNj3pbGU",
"spotify:artist:4yopgfi1zlVLWT2a1Cp3db",
"spotify:artist:283yDtIrgI9rixqFPwsyGE",
"spotify:artist:7JFLvUBiUQws6ub4qyJQN5",
"spotify:artist:1cQ0dsv72gTAuQLY3Pjm7A",
"spotify:artist:4PAzmaD8UjbH1eqbJFTst3",
"spotify:artist:2XqEqrO0lAfEXQxw1iGDEm",
"spotify:artist:47WFcgex0h7WBIjJlBKyHK",
"spotify:artist:3K0sJbNSKSNtWw1nTyUwes",
"spotify:artist:4zG6A8JAA3nWSGAWVRvZak",
"spotify:artist:5syLI88zOoytjZMzX2ukEJ",
"spotify:artist:0GNfGnAcX7ghBAvj2UlAqU",
"spotify:artist:3jIiTTxKMKWq4q1QiiR3Sk",
"spotify:artist:60WfuKYna3PpG6b6fxBuVJ",
"spotify:artist:5OzRYqc59hTyB6C3F1tc1r",
"spotify:artist:2gmqN8zeG1ryzXw8TXQIf5",
"spotify:artist:6OdRZw18BwNooaUp5vksZ5",
"spotify:artist:1t2WgRCERK2B8hdiry6oTM",
"spotify:artist:7qNB6bSJm89enGwovec5gT",
"spotify:artist:7MXjss6q8aHN0e0G8L9Yzt",
"spotify:artist:6OlAn6jcKPVCMa0oLSVDuc",
"spotify:artist:1DrwCWvEhlFaq5AnDWhgwK",
"spotify:artist:55Mkt4ikMa9bZrpaNJhaIs",
"spotify:artist:1ihgBlSUJXYEPeZ4upyhbh",
"spotify:artist:6iISeKHXtBE38lTOoABhX5",
"spotify:artist:77RbMXvBQIJpg9Levz6EDc",
"spotify:artist:4X9HpTsNnPpmtVD7dTnzev",
"spotify:artist:7IyZ3Ds2WGErYHb1BtouQZ",
"spotify:artist:6wJ6lfLOqbYk1bNH12s1Av",
"spotify:artist:7melmVxXBirB0ouGAQzHsE",
"spotify:artist:4505bCXcbaRNYq9K4pEKZG",
"spotify:artist:288wW7ANSue7owIGAdFoyU",
"spotify:artist:6WOeoPDV7qlEalMPT6Qewa",
"spotify:artist:1DvzZuRjAqpHoZYVn8Z6b7",
"spotify:artist:2vxQNKvFZYiS4et6I653Gw",
"spotify:artist:0yjAv7auR6T1vrkCaKfOrl",
"spotify:artist:6cIXH7XFZuekHfz9TsAnQN",
"spotify:artist:3IY2QnS5eMtCUUchI7DTW3",
"spotify:artist:3vmVpKM3mDIRrDRIUY5v0t",
"spotify:artist:6vHwhvQYzAtROIzAN8Qrtg",
"spotify:artist:3enTepNzfqb0375oy1yO0S",
"spotify:artist:0dMgVrJc29sbtATurmr77p",
"spotify:artist:7KLDzwuvugzv3alkXbTbYX",
"spotify:artist:4Fi9aXk2JSdDzwDtEKnCgh",
"spotify:artist:7vPlCwO3EdsYuBNQlvkSZw",
"spotify:artist:1VloWFpsDDa7fE3O9GwmP3",
"spotify:artist:6qTeg2kSXEuAqZOQxtH2Ki",
"spotify:artist:2rfrFAm67q8e2QKhkw7tVh",
"spotify:artist:3NFLyaND3kIecpoFtsBHVm",
"spotify:artist:0ni65wZGBs93VomXPAqHUw",
"spotify:artist:2BrB1yM0OCJlZDm74o6wW4",
"spotify:artist:6y3UPCAs2TReoWinmSG5tD",
"spotify:artist:2tFblYtXKLTFjvH1sxfbv1",
"spotify:artist:0c5oSm1mk90s6TCzezyUIQ",
"spotify:artist:40RucDSPGC6Ab8lYjkM65d",
"spotify:artist:2YsACQrJwicp5gxLJCF5tJ",
"spotify:artist:3hPg4RJ0xT1lpPqxnNmN3S",
"spotify:artist:1nB5iPH1myZ34AtRjdURVM",
"spotify:artist:7tuf0iv6yEP5PKfX1q0mTz",
"spotify:artist:74njzM4ODavqn93b92tavo",
"spotify:artist:5qGpv7J7Ud7c4sgGdSvmNA",
"spotify:artist:7qiLImHgYjwcdye5WpuH7I",
"spotify:artist:7gJQnsPcjwSfW6RC0Dii1R",
"spotify:artist:5Fna9v9xC8wPZ9XQ1AgYQr",
"spotify:artist:7u0CtQfowkJfjg2qysI3Ck",
"spotify:artist:1EyJWVJI3ileo0jyOEahBS",
"spotify:artist:2wUnt2CzuPOw8rFMxWBeGM",
"spotify:artist:2fZJ8yokGdLTllSp155FGU",
"spotify:artist:5eRZUpdMJrUrxd830TvCf2",
"spotify:artist:3Ib3NqgJEf4H7s3CCeYIta",
"spotify:artist:0biV7YWVxehXFzdpHKvlYw",
"spotify:artist:2yiqR74oxJCguoKvryuWJX",
"spotify:artist:4dKWXVJOUqKj8yUmUHHpra",
"spotify:artist:4GGidyZ5rd0jLsS9PMbSxu",
"spotify:artist:1wWL7F4LsqncYdaKP0QKJZ",
"spotify:artist:4yKFWuiwW5LEtWzkfBKsQv",
"spotify:artist:0uQUYaVFOhflrlh7ax8Bvw",
"spotify:artist:2rHewXpsj2T9K5kjIJzrc7",
"spotify:artist:3tMgmaEF1Sy8Wa2464DaKE",
"spotify:artist:20Zq6TTq9oPFCUS4HThEfM",
"spotify:artist:59YEEMCJiJZ037NJQRAsQp",
"spotify:artist:7naiCoWPrSNie0Tr3awKIe",
"spotify:artist:5oFcnaLzACIJb7Z5mRDe5D",
"spotify:artist:7wGSyJzvDzxQaCZJjGB9KL",
"spotify:artist:5719NrJrXAQeufe8TfQS2Z",
"spotify:artist:2WG8TPl4z6PxT6PBhX1XfF",
"spotify:artist:50EKhhvz9JxACblQKe46QR",
"spotify:artist:7iEX2UiUHHdMBE6f6pJjbC",
"spotify:artist:0JNyBluYV6HgUrTK2E0HHS",
"spotify:artist:3YjSgmMwjpc4p9c0kQbJcR",
"spotify:artist:78zcMhkVVWNZa25YOobRRZ",
"spotify:artist:1a4q2fXEL1FEAGyjU1ERxC",
"spotify:artist:3ZFG6h6BfwQCs1Ra8VFiYY",
"spotify:artist:0vCEmNYNkNhWq9KZ5ozL2c",
"spotify:artist:4BxXoA7toVG59lfB6HGSnM",
"spotify:artist:2K7i5FcqJw1D4GUf9OVldx",
"spotify:artist:098mxtf24z229B26eOAMji",
"spotify:artist:2qC48aQwvX4QwadR59ZNFj",
"spotify:artist:5IFhXYxYyhzRP61J6tiGkr",
"spotify:artist:1MLH2B4IQwZjeItwlyqMTW",
"spotify:artist:7i7Vof0M51945QH9dGTrXI",
"spotify:artist:2NPCXLXa4jrGnMkzoaYsbG",
"spotify:artist:64Q2dAXNdac9Zo6nw42oQj",
"spotify:artist:425hxm8974kyYgsDgcwEqf",
"spotify:artist:4BkS6aoEk0Nsvm5rXXIlJo",
"spotify:artist:5UQZtteP7G9PaRzif3jgEq",
"spotify:artist:5zBwriA9611Qf2dMqdKVyV",
"spotify:artist:1aDlHh1GQqjbqTKpQHDp38",
"spotify:artist:0RA47Eani3yO65ackVl2lW",
"spotify:artist:1K93XVC0EVwjWKUdHGheQ5",
"spotify:artist:6ohUlx8aPhjkt0TmrRgsbT",
"spotify:artist:7EuaQlWXpSdUXvENGjk9UV",
"spotify:artist:562nJv95sm1VixfqmZwc9M",
"spotify:artist:3gkeL6adn9QmmDiHLOHIoP",
"spotify:artist:0winpgMPcTi52eLFn0XGwz",
"spotify:artist:0l2Nh5pQJJ2vribfrv4EmO",
"spotify:artist:18lqRyyFbpClXNGZIaUZqt",
"spotify:artist:6buAFbi9bJw87XwLQu3H5Y",
"spotify:artist:7tqtGTQrMndlmY802nvHqs",
"spotify:artist:2YEhgeghg1uDLM4r3ltfFB",
"spotify:artist:28SrDp4kHT6KXcKHhuTzVU",
"spotify:artist:2J7wyJ1wjvfcWXtg4MpEdw",
"spotify:artist:5wW7idUzEz5cMhYnkLBaXM",
"spotify:artist:67CTyZGwkX71OypvrNml68",
"spotify:artist:3Mmr4QdzrNncdnkmPm4RDk",
"spotify:artist:4o47ZmpRcTKAY8JiCmGvVQ",
"spotify:artist:3H3rwMv31JYXvJOHFCSD1C",
"spotify:artist:1XPxQvbmobPQa0jhSZbZ7I",
"spotify:artist:6l11kbzGpVPlISGEPAZgNj",
"spotify:artist:4WVyczLYNzlYfrNE1MDGWa",
"spotify:artist:3INvKGTMnSBal7Z9FjUASS",
"spotify:artist:4thpVz9KWYTqJo65hrp9xI",
"spotify:artist:26tLH1Fb6GwDZ8buagYFyn",
"spotify:artist:22TNMfT78YinzBKTlPMEIi",
"spotify:artist:3MgtU3cRVBmjaF0BP6xPBD",
"spotify:artist:1CHssKUrijyH5WkJeYJwd8",
"spotify:artist:05e36qlGboObsoR5ifk5s4",
"spotify:artist:1O2N5HYjhOhXiI1Dsrb1FV",
"spotify:artist:0pHcON51YNq6OjLdo6azFO",
"spotify:artist:4m2Ls0DGT1ZdLMBpGAKXYx",
"spotify:artist:7L0j9vlZYWM0oV2OA6yeFl",
"spotify:artist:7dCg6XfmlOYrC9eHBDzC8t",
"spotify:artist:5LuGZGa4ZCydtgx6Xmo8vd",
"spotify:artist:0BG6WcB58QxdEhbbgQWlNd",
"spotify:artist:6dQFcx6vmpzeZpCucf345V",
"spotify:artist:7aSUCRetIIF7cr1rhdq8Ld",
"spotify:artist:49CEtoWUMbR88VqqnJzhhT",
"spotify:artist:1GWxRteTbATgqILjuLnoeS",
"spotify:artist:3OXJpReHkVw6RZlGuxuVUj",
"spotify:artist:0SXTtkeeScV06tGDLbqllB",
"spotify:artist:72B2tqZZCToukL3MRpyAhm",
"spotify:artist:1tYcc9xvoPTt97JkVrC5bF",
"spotify:artist:5e3XPHWo0Wv1kSBqVdCjeh",
"spotify:artist:2sgKD0ZfPAoTaNwHr8P6OD",
"spotify:artist:5ChZbGhGGfOFp1Ex9EQXlt",
"spotify:artist:4YPZL00JMkUuILCdX06DZY",
"spotify:artist:6CmUB2VnlV1mwPwTWATDHA",
"spotify:artist:4Jgnjl2FAvdmlTWxNsjOaH",
"spotify:artist:64UjbDl8MQvJDpPTFuzihC",
"spotify:artist:2LxQvEEBPxsLwhWHy9HJaz",
"spotify:artist:6komQpNvaXIbTDquMxIvzX",
"spotify:artist:52IfXnagF6XP85xYIXrmaz",
"spotify:artist:0D7nxgKM8AG9Wy9FDQOuOi",
"spotify:artist:30QlhzXScdQD2J7AhJaLc1",
"spotify:artist:1UpyUkz5xkuPJEODXQPGNo",
"spotify:artist:6DPS27TxYT0x3R2luYE4jk",
"spotify:artist:1vcsGNdC2TtOh0Tc64na8q"]


if __name__ == '__main__':
    from gemsearch.utils.slack import slack_send_message, slack_error_message
    
    logger.info('started missing artist crawler')  

    storage = Storage()
    artistCol = storage.getCollection('artists')
    sp = getSpotipyInstance()  

    for artistUri in missingIds:
        crawledArtist = crawlArtist(sp, artistUri)
                
        if crawledArtist is None:
            logger.warn('artists not found at api: ' + str(artistUri))
        else:
            artistCol.insert_one(crawledArtist)
            logger.info('crawled artist: %s', artistUri)
    
    slack_send_message('artist crawler is done')
