# Services and selectors

These rules apply to the Django backend. They are based on the
[HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide), with the
repository-specific constraints below taking precedence.

## Services

- Services are the write/business-logic path.
- A service may validate, create, update, delete, use transactions, call external resources, and
  trigger side effects.
- Services should be typed, use keyword-only arguments, and follow the `<entity>_<action>` naming
  convention, for example `project_create` or `membership_update`.
- Services must not import anything from `selectors`.

## Selectors

- Selectors are the read/query path.
- A selector may query the database and compose read results, but must not mutate data or trigger
  side effects.
- Selectors must not import anything from `services`.
- Selectors should be typed, use keyword-only arguments, and follow the `<entity>_<action>` naming
  convention, for example `project_get` or `membership_list`.

## Boundary rules

- Services and selectors are independent paths: neither may import the other, directly or
  indirectly.
- Do not solve a shared dependency by creating a service-selector cycle. Move genuinely shared,
  side-effect-free logic to a neutral module such as `domain.py` or `utils.py`.
- APIs, serializers, and views should remain thin: parse/validate transport data, call one service
  or selector, and serialize the result. Business logic belongs in services or selectors.

## Function inputs and outputs

- Every service and selector may accept and return only JSON-serializable data.
- Use primitives, `None`, lists, and dictionaries composed recursively from those values. Convert
  UUIDs, dates, datetimes, decimals, and other framework-specific values before crossing the
  boundary (for example, UUIDs and datetimes to strings).
- Pass identifiers and plain values, not Django model instances, QuerySets, managers, requests,
  serializers, uploaded files, or other framework objects.
- Never return Django models, QuerySets, model managers, serializers, HTTP responses, or other
  framework objects.
- A service may use Django models internally for persistence, but it must return a serialized
  result. A selector may use the ORM internally for reads, but it must return a serialized result.
- Prefer explicit typed result shapes such as `dict[str, object]` or `list[dict[str, object]]` and
  document their fields.

## Testing

- Test services and selectors through their public function boundaries.
- Service tests should verify writes, business rules, transactions, and side effects.
- Selector tests should verify filtering, visibility, ordering, and serialized output.
- Tests must also verify that service and selector results contain no Django model or ORM objects.
