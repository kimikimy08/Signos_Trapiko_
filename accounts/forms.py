from django import forms
from .models import User, UserProfile
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

class DateInput(forms.DateInput):
    input_type = 'date'
    

class UserForm(forms.ModelForm):
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Middle Name', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    mobile_number = forms.CharField(max_length=15, validators=[RegexValidator(
        '^\+[0-9]{1,3}\.?\s?\d{8,13}', message="Phone number must not consist of space and requires country code. eg : +639171234567")],widget=forms.TextInput(attrs={'placeholder': 'Mobile Number', 'class': 'form-control'}),
                                    error_messages={'unique': ("Mobile Number already exists.")})
    
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
                            error_messages={'unique': ("Email already exists.")},)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
                               error_messages={'unique': ("Username already exists.")},)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}), validators=[validate_password])
    #password = forms.CharField(validators=[MinLengthValidator(8),RegexValidator('^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z])$', message="Password should be a combination of Alphabets and Numbers")], widget=forms.PasswordInput(attrs={'placeholder': '********', 'style': 'width: 460px; '}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control' }))
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username', 'email', 'mobile_number', 'password']
        
    
        
    def clean(self):
        clean_data = super(UserForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        
        
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match!"
            )
    
    def save(self):
        self.clean()
        user = self.Meta.model(
            username = self.cleaned_data['username'], 
            email = self.cleaned_data['email'], 
        )
        user.set_password(self.cleaned_data['password2'])
        user.save()
        return user

class MemberForm(forms.ModelForm):
    birthdate = forms.DateField(widget=DateInput(attrs={'class': 'form-control ', }))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control p-1'} ) )
    upload_id = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control p-1'} ) )
    class Meta:
        model = UserProfile
        fields = ['birthdate', 'profile_picture']
    
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].required = False
        self.fields['upload_id'].required = False
        instance = getattr(self, 'instance', None)
        # if instance and instance.pk:
        #     self.fields['birthdate'].widget.attrs['readonly'] = True



class UserManagementForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username', 'email', 'mobile_number', 'password']

    ROLE_CHOICE = (
        (2, 'Admin'),
        (3, 'Super Admin')
    )
    
    ROLE_CHOICE_1 = (
        (1, 'Member'),
        (2, 'Admin'),
        (3, 'Super Admin')
    )
    
    STATUS_CHOICE = (
        (1, 'Pending'),
        (2, 'Active'),
        (3, 'Deactive')
    )
    
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Jones', 'class': 'form-control ', }))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'A', 'class': 'form-control', }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Smith', 'class': 'form-control',}))
    mobile_number = forms.CharField(max_length=15, validators=[RegexValidator(
        '^\+[0-9]{1,3}\.?\s?\d{8,13}', message="Phone number must not consist of space and requires country code. eg : +639171234567")],widget=forms.TextInput(attrs={'placeholder': '09123456789', 'class': 'form-control',}),
                                    error_messages={'unique': ("Mobile Number already exists.")})
    
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'jonesmith@gmail.com', 'class': 'form-control',}),
                            error_messages={'unique': ("Email already exists.")},)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}),
                               error_messages={'unique': ("Username already exists.")},)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}), validators=[validate_password])
    #password = forms.CharField(validators=[MinLengthValidator(8),RegexValidator('^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z])$', message="Password should be a combination of Alphabets and Numbers")], widget=forms.PasswordInput(attrs={'placeholder': '********', 'style': 'width: 460px; '}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********', 'class': 'form-control', }))
    role = forms.CharField(widget=forms.Select(choices=ROLE_CHOICE, attrs={ 'class': 'form-control', }))
    status = forms.CharField(widget=forms.Select(choices=STATUS_CHOICE, attrs={ 'class': 'form-control', }))
    


    def __init__(self, *args, **kwargs):
        ROLE_CHOICE_1 = (
        (1, 'Member'),
        (2, 'Admin'),
        (3, 'Super Admin')
        
        
    )
        
        super(UserManagementForm, self).__init__(*args, **kwargs)
        self.fields['role'].required = False
        self.fields['status'].required = False
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['role'].widget.choices = ROLE_CHOICE_1
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False
        
    def clean(self):
        clean_data = super(UserManagementForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        
        
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match!"
            )
    
    def save(self, commit=True):
        user = super(UserManagementForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password or confirm_password:
            user.set_password(password)
        if commit:
            user.save()
        return user



class UserManagementForm1(forms.ModelForm):
    
    ROLE_CHOICE = (
        (2, 'Admin'),
        (3, 'Super Admin')
    )
    
    ROLE_CHOICE_1 = (
        (1, 'Member'),
        (2, 'Admin'),
        (3, 'Super Admin')
    )
    
    STATUS_CHOICE = (
        (1, 'Pending'),
        (2, 'Active'),
        (3, 'Deactive')
    )
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Middle Name', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    mobile_number = forms.CharField(max_length=15, validators=[RegexValidator(
        '^\+[0-9]{1,3}\.?\s?\d{8,13}', message="Phone number must not consist of space and requires country code. eg : +639171234567")],widget=forms.TextInput(attrs={'placeholder': 'Mobile Number', 'class': 'form-control'}),
                                    error_messages={'unique': ("Mobile Number already exists.")})
    
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
                            error_messages={'unique': ("Email already exists.")},)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
                               error_messages={'unique': ("Username already exists.")},)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}), validators=[validate_password])
    #password = forms.CharField(validators=[MinLengthValidator(8),RegexValidator('^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z])$', message="Password should be a combination of Alphabets and Numbers")], widget=forms.PasswordInput(attrs={'placeholder': '********', 'style': 'width: 460px; '}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control' }))
    role = forms.CharField(widget=forms.Select(choices=ROLE_CHOICE, attrs={ 'class': 'form-control', }))
   
    
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username', 'email', 'mobile_number', 'password', 'role']
        
    
        
    def clean(self):
        clean_data = super(UserManagementForm1, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        
        
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match!"
            )
    
    def save(self):
        self.clean()
        user = self.Meta.model(
            username = self.cleaned_data['username'], 
            email = self.cleaned_data['email'], 
        )
        user.set_password(self.cleaned_data['password2'])
        user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    ROLE_CHOICE = (
        (1, 'Member'),
        (2, 'Admin'),
        (3, 'Super Admin')
    )
    
    STATUS_CHOICE = (
        (1, 'Pending'),
        (2, 'Active'),
        (3, 'Deactive')
    )
    # Feel free to add the password validation field as on UserCreationForm
    # username = forms.CharField(required=False, widget=forms.TextInput)
    # email = forms.CharField(required=False, widget=forms.TextInput)

    # password = forms.CharField(required=False, widget=forms.PasswordInput)
    # role = forms.CharField(required=False, widget=forms.Select(choices=ROLE_CHOICE, attrs={ 'class': 'form-control', }))
    # status = forms.CharField(required=False, widget=forms.Select(choices=STATUS_CHOICE, attrs={ 'class': 'form-control', }))
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Jones', 'class': 'form-control ', }))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'A', 'class': 'form-control', }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Smith', 'class': 'form-control',}))
    mobile_number = forms.CharField(max_length=15, validators=[RegexValidator(
        '^\+[0-9]{1,3}\.?\s?\d{8,13}', message="Phone number must not consist of space and requires country code. eg : +639171234567")],widget=forms.TextInput(attrs={'placeholder': '09123456789', 'class': 'form-control',}),
                                    error_messages={'unique': ("Mobile Number already exists.")})
    
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'jonesmith@gmail.com', 'class': 'form-control',}),
                            error_messages={'unique': ("Email already exists.")},)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}),
                               error_messages={'unique': ("Username already exists.")},)
    
    class Meta:
        model = User
        # Add all the fields you want a user to change
        fields = ('first_name', 'middle_name', 'last_name', 'mobile_number', 'username', 'email')
    
    def save(self, commit = True):
        user = super(UserUpdateForm, self).save(commit = False)
        user.mobile_number = self.cleaned_data['mobile_number']
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

            

class UserUpdateManagementForm(forms.ModelForm):
    ROLE_CHOICE = (
        (1, 'Member'),
        (2, 'Admin'),
        (3, 'Super Admin')
    )
    
    STATUS_CHOICE = (
        (1, 'Pending'),
        (2, 'Active'),
        (3, 'Deactive')
    )
    # Feel free to add the password validation field as on UserCreationForm
    # username = forms.CharField(required=False, widget=forms.TextInput)
    # email = forms.CharField(required=False, widget=forms.TextInput)

    # password = forms.CharField(required=False, widget=forms.PasswordInput)

    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Jones', 'class': 'form-control ', }))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'A', 'class': 'form-control', }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Smith', 'class': 'form-control',}))
    mobile_number = forms.CharField(max_length=15, validators=[RegexValidator(
        '^\+[0-9]{1,3}\.?\s?\d{8,13}', message="Phone number must not consist of space and requires country code. eg : +639171234567")],widget=forms.TextInput(attrs={'placeholder': '09123456789', 'class': 'form-control',}),
                                    error_messages={'unique': ("Mobile Number already exists.")})
    
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'jonesmith@gmail.com', 'class': 'form-control',}),
                            error_messages={'unique': ("Email already exists.")},)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}),
                               error_messages={'unique': ("Username already exists.")},)
    
    class Meta:
        model = User
        # Add all the fields you want a user to change
        fields = ('first_name', 'middle_name', 'last_name', 'mobile_number', 'username', 'email', 'role', 'status')
    
    def save(self, commit = True):
        user = super(UserUpdateManagementForm, self).save(commit = False)
        user.mobile_number = self.cleaned_data['mobile_number']
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user
    
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateManagementForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['first_name'].widget.attrs['readonly'] = True
            self.fields['middle_name'].widget.attrs['readonly'] = True
            self.fields['last_name'].widget.attrs['readonly'] = True
            self.fields['mobile_number'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['role'].widget.attrs['class'] = 'form-control'
            self.fields['status'].widget.attrs['class'] = 'form-control'

class ProfileMgmtUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(widget=DateInput(attrs={'class': 'form-control ', }))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control p-1'} ) )
    class Meta:
        model = UserProfile
        fields = ['birthdate', 'profile_picture']
    
    def __init__(self, *args, **kwargs):
        super(ProfileMgmtUpdateForm, self).__init__(*args, **kwargs)
        self.fields['birthdate'].required = False
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['birthdate'].required = False

class ProfileMgmtUpdateFormEdit(forms.ModelForm):
    birthdate = forms.DateField(widget=DateInput(attrs={'class': 'form-control ', }))
    upload_id = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control p-1'} ) )
    class Meta:
        model = UserProfile
        fields = ['birthdate']
    
    def __init__(self, *args, **kwargs):
        super(ProfileMgmtUpdateFormEdit, self).__init__(*args, **kwargs)
        self.fields['birthdate'].required = False
        self.fields['upload_id'].required = False
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['birthdate'].widget.attrs['readonly'] = True
            
class ProfileMgmtUpdateFormEdit_1(forms.ModelForm):
    birthdate = forms.DateField(widget=DateInput(attrs={'class': 'form-control ', }))
    upload_id = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control p-1'} ) )
    class Meta:
        model = UserProfile
        fields = ['birthdate', 'upload_id', 'profile_picture']
    
    def __init__(self, *args, **kwargs):
        super(ProfileMgmtUpdateFormEdit_1, self).__init__(*args, **kwargs)
        self.fields['birthdate'].required = False
        self.fields['upload_id'].required = False
        self.fields['profile_picture'].required = False
        instance = getattr(self, 'instance', None)
        
    

    

        