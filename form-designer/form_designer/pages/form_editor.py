import reflex as rx

import reflex_local_auth

from .. import routes, style
from ..components import navbar, form_select, form_editor, field_editor_modal


@reflex_local_auth.require_login
def form_editor_page() -> rx.Component:
    return style.layout(
        navbar(),
        rx.hstack(
            form_select(),
            rx.button(
                "New Form",
                on_click=rx.redirect(routes.FORM_EDIT_NEW),
                type="button",
            ),
            width="100%",
        ),
        rx.divider(),
        form_editor(),
        rx.cond(
            rx.State.form_id != "",
            rx.fragment(
                rx.button(
                    "Add Field",
                    on_click=rx.redirect(routes.edit_field(rx.State.form_id, "new")),
                    is_disabled=rx.State.form_id == "",
                    type="button",
                ),
                field_editor_modal(),
            ),
        ),
        rx.logo(height="3em", margin_bottom="12px"),
    )
