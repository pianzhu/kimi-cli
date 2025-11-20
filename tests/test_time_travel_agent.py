from kosong.message import Message, TextPart
from kosong.tooling import ToolError

import pytest

from kimi_cli.soul.context import Context
from kimi_cli.soul.denwarenji import DMail, DenwaRenji, DenwaRenjiError
from kimi_cli.tools.dmail import SendDMail


def _text_message(role: str, text: str) -> Message:
    return Message(role=role, content=[TextPart(text=text)])


def test_denwarenji_validates_checkpoint_range():
    denwa = DenwaRenji()
    denwa.set_n_checkpoints(2)
    dmail = DMail(message="hello", checkpoint_id=1)
    denwa.send_dmail(dmail)

    pending = denwa.fetch_pending_dmail()
    assert pending == dmail

    with pytest.raises(DenwaRenjiError):
        denwa.send_dmail(DMail(message="oops", checkpoint_id=5))


def test_denwarenji_rejects_multiple_pending():
    denwa = DenwaRenji()
    denwa.set_n_checkpoints(3)
    denwa.send_dmail(DMail(message="first", checkpoint_id=0))

    with pytest.raises(DenwaRenjiError):
        denwa.send_dmail(DMail(message="second", checkpoint_id=1))


@pytest.mark.asyncio
async def test_context_revert_to_truncates_history(tmp_path):
    ctx = Context(tmp_path / "ctx.jsonl")
    await ctx.checkpoint(add_user_message=True)
    await ctx.append_message(_text_message("assistant", "step-1"))
    await ctx.checkpoint(add_user_message=False)
    await ctx.append_message(_text_message("assistant", "step-2"))

    assert len(ctx.history) == 3
    assert ctx.n_checkpoints == 2

    await ctx.revert_to(1)

    assert [part.text for part in ctx.history[0].content] == ["<system>CHECKPOINT 0</system>"]
    assert len(ctx.history) == 2
    assert ctx.n_checkpoints == 1


@pytest.mark.asyncio
async def test_send_dmail_returns_tool_error_even_when_successful():
    denwa = DenwaRenji()
    denwa.set_n_checkpoints(4)
    tool = SendDMail(denwa)

    result = await tool(DMail(message="carry these insights", checkpoint_id=2))
    assert isinstance(result, ToolError)
    assert result.brief == "D-Mail not sent"

    pending = denwa.fetch_pending_dmail()
    assert pending is not None
    assert pending.message.startswith("carry")


@pytest.mark.asyncio
async def test_send_dmail_propagates_denwarenji_errors():
    denwa = DenwaRenji()
    denwa.set_n_checkpoints(1)
    tool = SendDMail(denwa)

    result = await tool(DMail(message="invalid", checkpoint_id=5))
    assert isinstance(result, ToolError)
    assert "Failed to send D-Mail" in result.brief
    assert denwa.fetch_pending_dmail() is None
