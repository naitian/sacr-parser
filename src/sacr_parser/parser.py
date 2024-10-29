"""
Parse a SACR file
"""

from __future__ import annotations

from dataclasses import dataclass

from lark import Lark, Transformer, Tree

from sacr_parser.utils import relative_path

Entity = str


@dataclass
class Span:
    start_idx: int
    end_idx: int
    text: str


@dataclass
class Annotation:
    """
    Represents an annotation in a SACR file.
    """

    content: list[Span | Annotation]
    entity: Entity
    tag: str

    @property
    def text(self):
        return "".join([span.text for span in self.content])

    @property
    def span(self):
        spans = [item if isinstance(item, Span) else item.span for item in self.content]
        start_idx = spans[0].start_idx
        end_idx = spans[-1].end_idx
        return Span(start_idx=start_idx, end_idx=end_idx, text=self.text)


class SACRTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.current_index = 0

    def annotation(self, items):
        # `items` is a list of parsed values in order
        if len(items) == 3:
            entity, tag_name, content = items
            tag_value = None
        elif len(items) == 4:
            entity, tag_name, tag_value, content = items
        else:  # Handle unexpected length
            raise ValueError("Unexpected number of items in annotation")
        annotation = Annotation(
            content=content,
            entity=entity,
            tag=f"{tag_name}={tag_value}",
        )
        return annotation

    def entity(self, items):
        # `items` is a list with one element (entity name as a token)
        return items[0].value

    def tag_name(self, items):
        return items[0].value

    def tag_value(self, items):
        return items[0].value

    def content(self, items):
        # content only has one item
        return items
        # content = [
        #     item.text if isinstance(item, Annotation) else item for item in items
        # ]
        # return Span(
        #     start_idx=content[0].start_idx,
        #     end_idx=content[-1].end_idx,
        #     text="".join([span.text for span in content]),
        # )

    def plain_text(self, items):
        text = items[0].value
        start_index = self.current_index
        self.current_index += len(text)
        end_index = self.current_index
        return Span(
            start_idx=start_index,
            end_idx=end_index,
            text=items[0].value,
        )


def find_annotations(root):
    if isinstance(root, Annotation):
        yield root
        for child in root.content:
            yield from find_annotations(child)
    if isinstance(root, Tree):
        for node in root.children:
            yield from find_annotations(node)


def parse(sacr_file: str) -> list[Annotation]:
    """
    Parse a SACR file and return a dictionary representation of its contents.

    Args:
        sac_file (str): The path to the SACR file to be parsed.

    Returns:
        dict: A dictionary representation of the SACR file contents.
    """

    grammar = open(relative_path("./sacr.lark")).read()
    parser = Lark(grammar, parser="lalr", start="start", transformer=SACRTransformer())

    tree = parser.parse(sacr_file)
    # search tree for annotations

    annotations = []
    for annotation in find_annotations(tree):
        annotations.append(annotation)

    return annotations


if __name__ == "__main__":
    # Example usage
    from sacr_parser.utils import BASE_DIR

    sample_sacr_file = open(BASE_DIR / "example/62.txt").read()
    print(parse(sample_sacr_file))
