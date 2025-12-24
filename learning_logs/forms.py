from django import forms
from  .models import Topic, Entry, Comment, Files, Images, ComplaintTopic, ComplaintComment


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text',]
        labels = {'text': '',}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Comment',}
        widgets = {'text': forms.Textarea(attrs={'cols': 80, 'rows':4}),}
        
        
class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['file']
        labels = {'file': 'File'}
        widgets = {'file': forms.ClearableFileInput()}
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 10 * 1024 * 1024:  # 10 MB limit
                raise forms.ValidationError("File size should not exceed 10 MB.")
            if not file.name.lower().endswith(('.pdf', '.doc', '.docx', '.txt',
                                               '.xls', '.xlsx', '.pptx', '.ppt',
                                               '.psd', '.zip', '.rar', 'mp3', 
                                               '.ogg', '.wav', '.aac', '.wma', 
                                               '.flac', '.wmv', '.mp4', '.webm', 
                                               '.mov', '.avi', '.flv')):
                raise forms.ValidationError("Unsupported file type.")
        return file
        
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']
        labels = {'image': 'Image'}
        widgets = {'image': forms.ClearableFileInput()}
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5 MB limit
                raise forms.ValidationError("Image size should not exceed 5 MB.")
            if not image.name.lower().endswith(('.jpg', '.svg', '.avif', '.psd', '.ai', '.png', '.gif', '.bmp', '.tiff', '.webp')):
                raise forms.ValidationError("Unsupported image type.")
        return image
        
        
class ComplaintTopicForm(forms.ModelForm):
    class Meta:
        model = ComplaintTopic
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop("owner", None)   # автор скарги
        self.topic = kwargs.pop("topic", None)   # тема на яку скаржаться
        self.offender = kwargs.pop("offender", None)  # порушник
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if ComplaintTopic.objects.filter(owner=self.owner, topic=self.topic).exists():
            raise forms.ValidationError("You have already filed a complaint about this topic.")

        return cleaned_data

    def save(self, commit=True):
        complaint = super().save(commit=False)
        complaint.owner = self.owner
        complaint.topic = self.topic
        complaint.offender = self.offender
        if commit:
            complaint.save()
        return complaint


class ComplaintCommentForm(forms.ModelForm):
    class Meta:
        model = ComplaintComment
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop("owner", None)   # автор скарги
        self.comment = kwargs.pop("comment", None)   # коментар на який скаржаться
        self.offender = kwargs.pop("offender", None)  # порушник
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if ComplaintComment.objects.filter(owner=self.owner, comment=self.comment).exists():
            raise forms.ValidationError("You have already filed a complaint about this comment.")

        return cleaned_data

    def save(self, commit=True):
        complaint = super().save(commit=False)
        complaint.owner = self.owner
        complaint.comment = self.comment
        complaint.offender = self.offender
        if commit:
            complaint.save()
        return complaint
