from model import model
from view import register_login_popup_view

from . import presenter


def main() -> None:
    main_model = model.Model()
    main_view = register_login_popup_view.RootView()
    main_presenter = presenter.Presenter(main_model, main_view)
    main_presenter.run()


if __name__ == "__main__":
    main()
