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
- Services may import and call selectors when they need read-side data for a write operation.

## Selectors

- Selectors are the read/query path.
- A selector may query the database and compose read results, but must not mutate data or trigger
  side effects.
- Selectors must not import or call services, directly or indirectly.
- Selectors should be typed, use keyword-only arguments, and follow the `<entity>_<action>` naming
  convention, for example `project_get` or `membership_list`.

## Boundary rules

- Services and selectors have an intentionally one-way dependency: services may depend on
  selectors, but selectors must never depend on services.
- Do not create a service-selector cycle. Move genuinely shared, side-effect-free logic to a
  neutral module such as `domain.py` or `utils.py`.

## Views and APIs

- Views/API endpoints are thin transport layers, not a place for business logic.
- A view may authenticate/authorize the request, parse and validate transport input, call one
  selector for reads or one service for writes, and serialize the response.
- Reads must be delegated to selectors; writes and state-changing operations must be delegated to
  services.
- Do not put business rules, ORM workflows, transactions, or side effects in views, viewsets, or
  serializers.
- Prefer one API endpoint per operation and simple `APIView` or `GenericAPIView` classes. Avoid
  abstractions that hide the service/selector call.
- Keep input and output serializers separate. Serializers validate and represent transport data;
  they do not implement domain behavior.

## Function inputs and outputs

- Every service and selector may accept only serializable data and may return only serializable
  data or a dedicated serializable DTO dataclass.
- DTO dataclasses must contain only primitives, `None`, lists, dictionaries, or nested DTO
  dataclasses composed recursively from those values. Convert UUIDs, dates, datetimes, decimals,
  and other framework-specific values before crossing the boundary (for example, UUIDs and
  datetimes to strings).
- Define service/selector DTO dataclasses in the app's `dtos.py` module. DTOs are the only allowed
  structured return type for services and selectors.
- DTO names must match the operation that returns them using the `<Operation>DTO` convention, for
  example `ProjectCreateDTO`, `ProjectUpdateDTO`, or `ProjectListDTO`.
- Do not use `Output` in DTO names. DTOs always represent service/selector output. If a dataclass
  is ever required for service/selector input, use a `<Operation>Payload` name instead.
- Pass identifiers and plain values, not Django model instances, QuerySets, managers, requests,
  serializers, uploaded files, or other framework objects.
- Never return Django models, QuerySets, model managers, serializers, HTTP responses, or other
  framework objects.
- A service may use Django models internally for persistence, but it must return a serialized
  result. A selector may use the ORM internally for reads, but it must return a serialized result.
- Prefer explicit typed DTO result shapes and document their fields.

## Exceptions

- Services and selectors must not raise Django, DRF, or serializer validation exceptions.
- Define app-specific exceptions in the relevant app's `exceptions.py` module and make them
  inherit from the shared base exceptions in `core/exceptions.py`.
- Do not create app-specific catch-all base exceptions such as `ProjectError`; use the shared
  exception hierarchy instead.
- The central exception handler maps `BusinessRuleError` to HTTP 400 and `EntityNotFoundError` to
  HTTP 404, and `PermissionDeniedError` to HTTP 403. Exception classes must not contain HTTP
  status codes.
- A central DRF exception handler translates business exceptions into HTTP responses; views should
  not catch and remap domain exceptions themselves.

## Testing

- Test services and selectors through their public function boundaries.
- Service tests should verify writes, business rules, transactions, and side effects.
- Selector tests should verify filtering, visibility, ordering, and serialized output.
- Tests must also verify that service and selector results contain no Django model or ORM objects.

## Documentation

- Add concise, meaningful Google-style docstrings to every production class and function.
- Include `Args`, `Returns`, and `Raises` sections when they add useful information; do not add
  empty or redundant sections.
- Test functions do not require docstrings.

## Import conventions

- Use relative imports for dependencies inside the same Django module/app. For example, code in
  `apps.project` should import `Project` from `apps.project.models` using `from .models import
  Project` or `from ..models import Project`, depending on the package depth.
- Use absolute imports for dependencies across Django modules. For example, code in `apps.project`
  importing from `core` should use `from core.exceptions import ApplicationError`.
- Do not use absolute imports for same-module dependencies or relative imports to cross module
  boundaries.

## Module size and structure

- Keep modules focused on one responsibility.
- When a file starts to grow or contains more than one substantial class, split it into focused
  modules, especially for views, services, selectors, models, and serializers.
- Group related modules in a package with an `__init__.py` that exports the public classes or
  functions.
- Name split view modules after the resource and operation, for example
  `project_collection_api.py` or `project_detail_api.py`.
