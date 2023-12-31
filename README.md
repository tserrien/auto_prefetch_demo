# The big 1+N problem solving showdown
The goal of this project is to showcase the (proper) usage of [django-auto-prefetch](https://pypi.org/project/django-auto-prefetch/) through examples.
The project is intended to assist me in providing an example to colleagues, but it's a great opportunity to give back to the community.  
Hope you learn something reading the code and resources!

<!-- TOC -->
* [The big 1+N problem solving showdown](#the-big-1n-problem-solving-showdown)
* [Okay, okay, but what's the fuss about?](#okay-okay-but-whats-the-fuss-about)
  * [Project scope](#project-scope)
  * [What the project is NOT about:](#what-the-project-is-not-about)
  * [The 1+N query problem in a nutshell](#the-1n-query-problem-in-a-nutshell)
  * [Potential solutions](#potential-solutions)
    * [Manual prefetching only where needed](#manual-prefetching-only-where-needed)
    * [Using django-auto-prefetch](#using-django-auto-prefetch)
  * [Conclusion:](#conclusion)
  * [Found a mistake? Should I look into something more exotic in admin?](#found-a-mistake-should-i-look-into-something-more-exotic-in-admin)
* [Running the project locally](#running-the-project-locally)
<!-- TOC -->

# Okay, okay, but what's the fuss about?

When using Object-relational mapping in your chosen framework (in this case Django) due to the decoupled nature of
the python code and the database layer it's easy to forget about the underlying SQL queries. This abstraction helps to
speed up development but _may_ have negative effect on the performance of your backend.    

## Project scope

This project aims to explore possible performance improvements of using a custom manager and the `django-auto-prefetch`
library mentioned above. I hope to see  significant savings in number of queries ran on querysets,
api endpoints and admin views. 

## What the project is NOT about:
Methods to detect occurrences of 1+N query related performance issues.  

Comparing memory usage on the database or application layer is not part of this benchmark.
The latter may be added later once I get more comfortable with [Scalene](https://pypi.org/project/scalene/).
Not to be expected in the near future though.

## The 1+N query problem in a nutshell

[//]: # (TODO: write nice example/explanation)

Ps: the readme of django-auto-prefetch has some nice reading material, incl. the debate over including this feature in django ~~don't get your hopes up~~.

## Potential solutions
One solution is to create a ticket in your choice of project management system, add `tech-debt` to the tags,
and elegantly sweep the problem under the rug until the problem is really eating into your resources. Ooooor you can
attempt to deal with it.

To keep comparisons similar the DRY principle was thrown out of the window. Many issues could be fixed with attention to
individual problems. The focus is on low-code solutions with high impact on performance. 

### Manual prefetching only where needed
This approach requires case-by-case analysis of every problematic endpoint and finding the underperforming query. Plenty
of analytics tools are available to detect this problem.

| Pros                                                                        | Cons                                                  |
|-----------------------------------------------------------------------------|-------------------------------------------------------|
| Only deals with one problematic point at a time                             | Only deals with one problematic point at a time       |
| Can deal with reverse FK query problems                                     | Manager methods or individual in-place fixes required |
| Can fix many-to-many type queries (in combination with `.select_related()`) | Time-consuming                                        |
|                                                                             | Does not apply to neither endpoints nor admin views   |

Coming soon:
Admin and views for this app as well to see how much extra code is required even in a simple app like this for comparable results.
Goal: Low effort (no custom querysets) and high effort (with custom querysets) versions

### Using django-auto-prefetch
This approach requires finding all your models with ForeignKey fields, changing/adding a few imports and potentially
fixing your already existing managers. Interactions of the package and pre-existing managers is not tested in this
project. Please refer to the original docs.

| Pros                                                                                            | Cons                                          |
|-------------------------------------------------------------------------------------------------|-----------------------------------------------|
| Almost [plug-and-play](https://www.meme-arsenal.com/memes/321b3cdd8d21162edff6e3529c988d66.jpg) | One more layer of complexity added to the ORM |
| Can't forget to use prefetch                                                                    | Doesn't deal with many-to-many relationships  |
| Serializers also benefit from the package                                                       |                                               |
| Massive savings in admin views where related fields appear on changelist views                  |                                               |


## Conclusion:
`django-auto-prefetch` is an excellent package to tackle 1+N query related performance issues. While it further adds to
the black-box nature of Django's ORM it helps in environments where time is at premium cost or engineers lack the
skill/insight to tackle this problem query by query.

The extra library also means an extra liability in case the package falls out of maintenance. The project is however currently under [regular maintenance](https://pypi.org/project/django-auto-prefetch/#history).

## Found a mistake? Should I look into something more exotic in admin?

Open a pr or issue!



Disclaimer:
I've chosen to test only with `ForeignKey` fields as in my day-to-day I'm yet to meet a OneToOne field.

I do not have any personal, professional or financial connection to any of the sources linked.


# Running the project locally

- Open a terminal in the project root
- Create and launch [virtual environment](https://docs.python.org/3/library/venv.html)
- Create a `.env` file in project root. Copy contents of `.env.example` into it.
- Generate a django secret key ([guide](https://www.educative.io/answers/how-to-generate-a-django-secretkey))

To start the development server:
```shell
cd prefetch
```
```shell
python manage.py runserver
```

To run the tests:
if not already in <root>/prefetch:
```shell
cd prefetch
```
Pytest is configured to my taste. Settings can be found in `pytest.ini`. [Docs](https://docs.pytest.org/en/latest/reference/customize.html) for customization
```shell
pytest
```

