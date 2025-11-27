from django import forms
from  .models import Topic, Entry, Files, Images, Complaint


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
        
        
class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['file']
        labels = {'file': 'File'}
        widgets = {'file': forms.ClearableFileInput()}
        
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']
        labels = {'image': 'Image'}
        widgets = {'image': forms.ClearableFileInput()}
        
        
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop("owner", None)   # автор скарги
        self.topic = kwargs.pop("topic", None)   # тема на яку скаржаться
        self.offender = kwargs.pop("offender", None)  # порушник
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if Complaint.objects.filter(owner=self.owner, topic=self.topic).exists():
            raise forms.ValidationError("Ви вже залишали скаргу на цю тему.")

        return cleaned_data

    def save(self, commit=True):
        complaint = super().save(commit=False)
        complaint.owner = self.owner
        complaint.topic = self.topic
        complaint.offender = self.offender
        if commit:
            complaint.save()
        return complaint
