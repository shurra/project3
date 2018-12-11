from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Category, PizzaTopping, SubsAddition, Sub, Pasta, Salad, DinnerPlatter, Order


class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    # username = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    # first_name = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    #                              max_length=32, help_text='First name')
    # last_name = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    #                             max_length=32, help_text='Last name')
    email = forms.EmailField(max_length=64, help_text='Enter a valid email address', required=True, label='e-mail',)
    # password1 = forms.CharField(forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    # password2 = forms.CharField(forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


class PizzaForm(forms.Form):
    # name = forms.CharField(max_length=100)
    # categories = Category.objects.exclude(name="Toppings")
    categories = Category.objects.filter(name__contains="Pizza")
    field_category = forms.ModelChoiceField(queryset=categories,
                                            required=True,
                                            empty_label="Select pizza")
    SIZES = (('1', 'Small'),
             ('2', 'Large'),
             )
    size = forms.ChoiceField(required=True, choices=SIZES)
    pizza_toppings = PizzaTopping.objects.all()
    toppings = forms.ModelMultipleChoiceField(queryset=pizza_toppings,
                                              required=False,
                                              widget=forms.CheckboxSelectMultiple)
    quantity = forms.IntegerField(required=True, initial=1, min_value=1, max_value=10)
    prefix = "pizza"

    def clean_toppings(self):
        toppings = self.cleaned_data.get('toppings')
        if toppings.count() > 5:
            raise forms.ValidationError("You can't select more than 5 toppings.")
        return toppings


class SubForm(forms.Form):
    subs = Sub.objects.all()
    name = forms.ModelChoiceField(queryset=subs, required=True, empty_label="Select sub")
    SIZES = (('1', 'Small'),
             ('2', 'Large'),
             )
    size = forms.ChoiceField(required=True, choices=SIZES, )
    extra_cheese = forms.BooleanField(required=False)
    subs_additions = SubsAddition.objects.all()
    addition = forms.ModelMultipleChoiceField(queryset=subs_additions,
                                              required=False,
                                              widget=forms.CheckboxSelectMultiple)
    quantity = forms.IntegerField(required=True, initial=1, min_value=1, max_value=10)
    prefix = "sub"


class PastaForm(forms.Form):
    pastas = Pasta.objects.all()
    name = forms.ModelChoiceField(queryset=pastas, required=True, empty_label="Select pasta")
    quantity = forms.IntegerField(required=True, initial=1, min_value=1, max_value=10)
    prefix = "pasta"


class SaladForm(forms.Form):
    salads = Salad.objects.all()
    name = forms.ModelChoiceField(queryset=salads, required=True, empty_label="Select salad")
    quantity = forms.IntegerField(required=True, initial=1, min_value=1, max_value=10)
    prefix = "salad"


class DinnerPlatterForm(forms.Form):
    dinner_platter = DinnerPlatter.objects.all()
    name = forms.ModelChoiceField(queryset=dinner_platter, required=True, empty_label="Select platter")
    SIZES = (('1', 'Small'),
             ('2', 'Large'),
             )
    size = forms.ChoiceField(required=True, choices=SIZES, )
    quantity = forms.IntegerField(required=True, initial=1, min_value=1, max_value=10)
    prefix = "dinner_platter"


class OrderForm(forms.ModelForm):
    done = forms.BooleanField()

    class Meta:
        model = Order
        fields = ['done']
