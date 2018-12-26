document.addEventListener('DOMContentLoaded', () => {
    var additions_div = document.querySelector('#id_sub-addition').parentElement;
    var subSelect = document.querySelector('#id_sub-name');
    var subSize = document.querySelector('#id_sub-size');
    additions_div.style.display = 'none';
    subSelect.addEventListener('change', () => {
        if (event.target.options[event.target.selectedIndex].text.includes("Steak") ) {
            additions_div.style.display = 'block';
        } else {
            additions_div.style.display = 'none';
        }
        if (event.target.options[event.target.selectedIndex].text.includes("Sausage, Peppers & Onions") ) {
            subSize.value = 2;
            subSize.parentElement.style.display = 'none';
        } else {
            subSize.value = 1;
            subSize.parentElement.style.display = 'block';
        }
    });
    var pizza_toppings_ul = document.querySelector('#id_pizza-toppings');
    var pizza_toppings_checkboxes = document.getElementsByName('pizza-toppings');
    var max_allowed = 5;
    pizza_toppings_checkboxes.forEach((item) => {
        item.addEventListener('change', () => {
            // console.log(pizza_toppings_ul.querySelectorAll('input[type="checkbox"]:checked').length);
            if (pizza_toppings_ul.querySelectorAll('input[type="checkbox"]:checked').length >= max_allowed) {
                pizza_toppings_ul.querySelectorAll('input[type="checkbox"]:not(:checked)').forEach((el) => {
                    el.disabled = true;
                });
            }
            else {
                pizza_toppings_ul.querySelectorAll('input[type="checkbox"]:not(:checked)').forEach((el) => {
                    el.disabled = false;
                })}
        });
    });

});
