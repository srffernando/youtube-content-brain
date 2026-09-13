from __future__ import annotations

from content_brain.domain.models import (
    Confidence,
    ContentDraft,
    HookCandidate,
    PsychologyInsight,
    Story,
    ThumbnailConcept,
    TitleCandidate,
    VideoFormat,
)
from content_brain.providers.base import LLMProvider


class MockProvider(LLMProvider):
    """Deterministic, realistic provider for demos and reliable tests."""

    name = "mock"
    model = "deterministic-v1"

    def generate(self, topic: str, format_: VideoFormat) -> ContentDraft:
        hooks = [
            HookCandidate(text="You know what to do - so why does starting feel impossible?", rationale="Names the central contradiction immediately."),
            HookCandidate(text="The real reason procrastination can feel harder than doing nothing.", rationale="Creates curiosity around a familiar frustration."),
            HookCandidate(text="If guilt could make you productive, you would be finished by now.", rationale="Uses a surprising, empathetic reframing."),
            HookCandidate(text="This is not laziness. It is a short-term relief loop.", rationale="Offers a clear counterintuitive explanation."),
            HookCandidate(text="Before you call yourself lazy, notice what you are avoiding.", rationale="Invites self-reflection and promises a useful shift."),
        ]
        titles = [
            TitleCandidate(text="Why You Procrastinate Even When You Know Better", rationale="Directly mirrors the viewer's dilemma."),
            TitleCandidate(text="Procrastination Is Not Laziness - Here Is Why", rationale="Strong reframe with clear payoff."),
            TitleCandidate(text="The Real Reason Starting Feels So Hard", rationale="Curiosity-led and emotionally relevant."),
            TitleCandidate(text="Why Guilt Never Fixes Procrastination", rationale="Specific emotional angle for the topic."),
            TitleCandidate(text="What Your Brain Is Avoiding When You Put Things Off", rationale="Specific question framed around behavior."),
        ]
        insights = [
            PsychologyInsight(
                claim="Procrastination can function as a way to escape an unpleasant feeling in the moment.",
                evidence_or_reasoning="Avoiding a difficult task can quickly reduce discomfort, which can make avoidance more likely the next time similar discomfort appears.",
                confidence=Confidence.MEDIUM,
                recommended_wording="One useful way to view procrastination is as short-term emotion management, not simply a failure of planning.",
            )
        ]
        if format_ is VideoFormat.LONG_FORM:
            insights.extend([
                PsychologyInsight(claim="Vague tasks often create more resistance than concrete next actions.", evidence_or_reasoning="A task such as 'write the report' contains many undecided steps; choosing one visible action reduces ambiguity.", confidence=Confidence.MEDIUM, recommended_wording="When a task feels foggy, making the first physical action specific can make it easier to begin."),
                PsychologyInsight(claim="Self-criticism may intensify avoidance when it adds threat to an already uncomfortable task.", evidence_or_reasoning="Harsh self-talk can turn a task into evidence about personal worth, increasing the emotional cost of engaging with it.", confidence=Confidence.MEDIUM, recommended_wording="Rather than treating delay as proof that you are broken, try treating it as a signal to reduce the next step."),
            ])
        story = Story(
            summary="A capable person opens an important task, feels a flash of pressure, and reaches for a smaller distraction that offers immediate relief.",
            beats=["An important task sits open.", "Pressure and uncertainty rise.", "A harmless distraction offers instant relief.", "The relief fades and guilt arrives.", "The next action is made smaller and concrete."],
            examples=["A student opens a blank assignment and starts reorganizing notes instead.", "An employee delays one difficult email by clearing easy notifications."],
            pattern_interrupts=["Pause: what feeling appears one second before you switch tasks?", "Try this: name the next action in five words."],
        )
        return ContentDraft(
            audience_pain="People feel stuck between knowing an important task matters and repeatedly choosing tiny distractions, then blaming themselves for the delay.",
            emotional_angle="Relief before guilt: procrastination is framed with compassion as a short-term escape from discomfort.",
            hooks=hooks,
            story=story,
            psychology_insights=insights,
            lesson="Do not argue with yourself into action. Shrink the task until the next step feels safe enough to start.",
            cta="Comment with the one task you will reduce to a two-minute first step today.",
            titles=titles,
            thumbnail=ThumbnailConcept(visual="Split image: a person staring at a laptop on one side and scrolling a phone on the other, with a visible unfinished checklist.", text_overlay="NOT LAZY", rationale="The visual contrast makes avoidance recognizable while the short text delivers the core reframe."),
            final_script=_script(topic, format_),
        )


def _script(topic: str, format_: VideoFormat) -> str:
    short = f"""You know what to do - so why does starting feel impossible? {topic} Imagine opening the task, feeling pressure in your chest, then checking one tiny thing on your phone. For a moment, the pressure drops. That relief is the trap: your brain learns that avoiding the task changes the feeling fast. This does not mean you are lazy. It may mean the task feels too vague, too risky, or too loaded. Instead of promising to finish everything, choose the smallest visible move: open the document, write one messy sentence, or set a two-minute timer. Starting is the payoff. Comment with the task you will shrink today."""
    if format_ is VideoFormat.SHORT:
        return short
    sections = [
        f"{topic} It is tempting to treat this as a discipline problem. But that explanation misses a familiar moment: you sit down with an important task, and before you make progress, you feel pressure. The task might be a report, an application, a hard conversation, or a decision you have delayed for weeks.",
        "Chapter one: the relief loop. Picture a student opening a blank assignment. The empty page suggests uncertainty, judgment, and the possibility of doing it badly. The student reorganizes notes instead. That action is not useless, but it provides a quick drop in discomfort. The brain notices the immediate relief. Next time the blank page appears, distraction becomes easier to choose.",
        "Pattern interrupt: pause and ask what feeling arrives just before you switch tasks. Is it confusion? Fear of a poor result? Boredom? The answer does not need to be dramatic. Naming it matters because it turns a vague accusation—'I am lazy'—into a workable observation—'this step feels unclear.'",
        "Chapter two: make the next action physical. 'Finish the presentation' is not an action; it is a cloud of decisions. 'Open the slide deck and write three ugly bullets' is an action. The smaller instruction removes some uncertainty without pretending the whole project is easy. A worker delaying a difficult email can write only the subject line. A person avoiding exercise can put on shoes and walk to the door.",
        "Here is another example. A creator wants to publish a video but keeps researching equipment. Research feels responsible, and sometimes it is. But if it replaces recording the first draft, it becomes a polished form of avoidance. The useful question is not 'Is this task productive?' It is 'Does this move reduce the real next step, or postpone it?'",
        "Chapter three: guilt adds weight. Self-criticism can make an unfinished task feel like evidence about your character. Then starting is no longer just work; it feels like a verdict. A more useful response is compassionate and practical: the task created friction, so lower the friction. Remove one decision, reduce one commitment, and create one visible start.",
        "Try a two-minute experiment. Write down the task. Beneath it, write the smallest action that would create evidence of motion. Set a timer for two minutes. When it ends, you may stop. The purpose is not to trick yourself into a marathon. It is to teach your attention that beginning does not have to be a threat.",
        "The lesson is simple: procrastination often makes sense as short-term emotion management. Once you see the loop, you can interrupt it with a smaller, clearer action. You do not need a perfect mood before you begin. You need a next step that is safe enough to attempt. Comment with the task you will reduce to a two-minute first step today, and save this for the next time guilt tries to run the plan.",
    ]
    # Repeat varied teaching beats to reach an 8–15 minute spoken script without external generation.
    expansion = []
    for index in range(8):
        expansion.append(f"Example {index + 1}: notice the moment after resistance appears. Instead of negotiating with every thought, make the next action smaller. Open the file, choose one sentence, or place the needed item on the desk. Small actions are not trivial when they break an avoidance loop; they are evidence that the task is now approachable.")
        expansion.append("A useful check is to separate preparation from progress. Preparation has a clear end and supports the next action. Avoidance expands endlessly and protects you from the discomfort of being seen as a beginner. Choose a boundary, then return to the visible action.")
    return "\n\n".join(sections[:3] + expansion + sections[3:])
