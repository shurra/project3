from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Category, PizzaTopping, SubsAddition, Sub, Pasta, Salad, DinnerPlatter, Order


class RegisterForm(UserCreationForm):
    # username = forms.CharField(required=True)
    email = forms.EmailField(max_length=64,
                             help_text='Enter a valid email address',
                             required=True,
                             label='Email address',)

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


class ProfileForm(UserChangeForm):
    # password = None

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
        exclude = ('password',)


# class ProfileForm(forms.ModelForm):
#
#     class Meta:
#         model = User
#         fields = (
#             'first_name',
#             'last_name',
#             'email',
#         )
