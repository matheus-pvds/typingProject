from main import MyFrame

myframe = MyFrame()
passage, author = myframe.extract_text_from_passage()
print("Quote:", passage)
print("Author:", author)