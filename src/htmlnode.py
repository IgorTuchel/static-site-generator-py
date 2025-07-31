class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented()

    def props_to_html(self):
        represent = ''
        if self.props:
            for element in self.props:
                represent += f' {element}="{self.props[element]}"'
        return represent
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.value == None and self.tag != "img":
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return f'{self.value}'
        
        tag_construct = f'<{self.tag}{self.props_to_html()}>'
        end_tag_constuct = f'</{self.tag}>'
        html_construct = f'{tag_construct}{self.value}{end_tag_constuct}'
        return html_construct
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.children:
            raise ValueError("No Child Nodes in ParentNode")
        if self.tag == None:
            raise ValueError("Invalid HTML: no tag")
        
        tag_construct = f'<{self.tag}{self.props_to_html()}>'
        child_content = ''
        for children in self.children:
            child_content += children.to_html()
        
        end_tag_constuct = f'</{self.tag}>'
        html_construct = f'{tag_construct}{child_content}{end_tag_constuct}'
        return html_construct