class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict[str, str] | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        res = ""
        if not self.props:
            return res
        for key in self.props:
            res += f' {key}="{self.props[key]}"'
        return res
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf node must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
         
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

