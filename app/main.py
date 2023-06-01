import os
import sys


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))

    from app.frontend import Frontend
    from app.backend import Backend

    backend = Backend()
    app = Frontend(backend)
    app.run()
