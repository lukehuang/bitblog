from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name
from django.utils.safestring import mark_safe
from markdown import markdown
from wagtail.wagtailcore import blocks
from docutils.core import publish_parts
from wagtail.wagtailcore import blocks


class CodeBlock(blocks.StructBlock):
    """
    Code Highlighting Block
    """

    LANGUAGE_CHOICES = (
        ('python', 'Python'),
        ('javascript', 'Javascript'),
        ('json', 'JSON'),
        ('bash', 'Bash/Shell'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('scss', 'SCSS'),
        ('yaml', 'YAML'),
    )

    language = blocks.ChoiceBlock(choices=LANGUAGE_CHOICES)
    code = blocks.TextBlock()

    class Meta:
        icon = 'code'

    def render(self, value):
        src = value['code'].strip('\n')
        lang = value['language']

        lexer = get_lexer_by_name(lang)
        formatter = get_formatter_by_name(
            'html',
            linenos=None,
            cssclass='codehilite',
            style='default',
            noclasses=False,
        )
        return mark_safe(highlight(src, lexer, formatter))


class MarkDownBlock(blocks.TextBlock):
    """
    A MarkDown block for Wagtail streamfields.
    """

    class Meta:
        icon = 'code'

    def render_basic(self, value):
        md = markdown(
            value,
            [
                'markdown.extensions.fenced_code',
                'codehilite',
            ],
        )
        return mark_safe(md)


class RSTBlock(blocks.TextBlock):
    """
    A ReSTructured text block for Wagtail streamfields.
    """

    class Meta:
        icon = 'code'

    def render_basic(self, value):
        return publish_parts(value, writer_name='html')['body']