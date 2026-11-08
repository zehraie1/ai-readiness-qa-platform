"""Import every model module so metadata is complete (used by Alembic and tests)."""

from app.modules.attempts import models as attempts_models  # noqa: F401
from app.modules.auth import models as auth_models  # noqa: F401
from app.modules.content import models as content_models  # noqa: F401
from app.modules.scoring import models as scoring_models  # noqa: F401
from app.modules.tracks import models as tracks_models  # noqa: F401
