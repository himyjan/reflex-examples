import reflex as rx

from reflex_local_auth import require_login

from .. import constants, style, utils
from ..components import field_prompt
from ..models import Form, Response
from ..state import AppState


class ResponsesState(AppState):
    form: Form = Form()
    responses: list[Response] = []

    def load_responses(self):
        if not self.is_authenticated:
            return
        with rx.session() as session:
            form = session.get(Form, self.form_id)
            if not self._user_has_access(form) or form is None:
                self.form = Form()
                return
            self.form = form
            self.responses = session.exec(
                Response.select().where(Response.form_id == self.form_id)
            ).all()

    def delete_response(self, id: int):
        if not self._user_has_access():
            return
        with rx.session() as session:
            session.delete(session.get(Response, id))
            session.commit()
            return ResponsesState.load_responses


def response_content(response: Response):
    return rx.vstack(
        rx.moment(value=response.ts, margin_bottom="2em"),
        rx.foreach(
            response.field_values,
            lambda fv: rx.vstack(
                field_prompt(fv.field),
                rx.cond(
                    fv.value != "",
                    rx.text(fv.value),
                    rx.text("No response provided."),
                ),
                align="start",
                margin_bottom="2em",
            ),
        ),
    )


def response(r: Response):
    return rx.accordion.item(
        header=rx.hstack(
            rx.text(r.client_token),
            rx.tooltip(
                rx.button(
                    rx.icon(tag="x", size=16),
                    color_scheme="tomato",
                    margin_right="1em",
                    on_click=ResponsesState.delete_response(r.id),
                ),
                content="Delete this Response",
            ),
            width="100%",
            justify="between",
        ),
        content=response_content(r),
        value=r.id.to(str),
    )


def responses_title():
    form_name = rx.cond(
        rx.State.form_id == "",
        utils.quoted_var("Unknown Form"),
        ResponsesState.form.name,
    )
    return f"{constants.TITLE} | {form_name} | Responses"


@require_login
def responses_page():
    return style.layout(
        rx.heading(ResponsesState.form.name),
        rx.accordion.root(
            rx.foreach(
                ResponsesState.responses,
                response,
            ),
            collapsible=True,
            type="multiple",
            width="100%",
            variant="outline",
        ),
    )
