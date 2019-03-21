function AddToCard() {
  var cur = document.getElementById("cart_count").innerHTML;
  if (cur != 0) {
    document.getElementById("cart_count").innerHTML = parseInt(cur) + 1;
  }
  else {
    document.getElementById("cart_count").innerHTML = 0;
  }
}

function ShowModal() {
  var url = window.location.href;
  if (url.indexOf('?openLogin') != -1 || url.indexOf('/openLogin') != -1) {
      $('#login').modal('show');
  }
}

function initImage() {
  var images = $('.image_list li');
  var selected = $('.image_selected img');

  images.each(function()
  {
    var image = $(this);
    image.on('click', function()
    {
      var imagePath = new String(image.data('image'));
      selected.attr('src', imagePath);
    });
  });
}

function updateTotal() {
  var quantity = document.getElementById("quantity_input").value;
  var price = parseFloat(document.getElementById("price").innerHTML);

  if (quantity != null) {
    document.getElementById("pricetopay").innerHTML = parseFloat(quantity*price).toFixed(2);
  }
  else {
    quantity = 1;
    document.getElementById("pricetopay").innerHTML = parseFloat(quantity*price).toFixed(2);
  }
}

function updateWishCount() {
  var wishCounter = parseInt(document.getElementById("wish_counter").innerHTML);
  document.getElementById("wish_counter").innerHTML = wishCounter + 1;
}

function initIsotope()
{
  var sortingButtons = $('.shop_sorting_button');

  $('.product_grid').isotope({
    itemSelector: '.product_item',
          getSortData: {
            price: function(itemElement)
            {
              var priceEle = $(itemElement).find('.product_price').text().replace( '£', '' );
              return parseFloat(priceEle);
            },
            name: '.product_name div a'
          },
          animationOptions: {
              duration: 750,
              easing: 'linear',
              queue: false
          }
      });

      // Sort based on the value from the sorting_type dropdown
      sortingButtons.each(function()
      {
        $(this).on('click', function()
        {
          $('.sorting_text').text($(this).text());
          var option = $(this).attr('data-isotope-option');
          option = JSON.parse(option);
      $('.product_grid').isotope(option);
        });
      });
}

function updLink() {
  var fnl = '';
    var link = document.getElementById('tocart').href;
    var quantity = document.getElementById('quantity_input').value;
    var fnl = link.slice(0, -1) + quantity.toString();
    document.getElementById('tocart').href = fnl;
    updateTotal();
}


(function() {
'use strict';

window.addEventListener('load', function() {
  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.getElementsByClassName('needs-validation');

  // Loop over them and prevent submission
  var validation = Array.prototype.filter.call(forms, function(form) {
	form.addEventListener('submit', function(event) {
	  if (form.checkValidity() === false) {
		event.preventDefault();
		event.stopPropagation();
	  }
	  form.classList.add('was-validated');
	}, false);
  });
}, false);
})();

$(window).load(function(){
   NProgress.done();
});

$(document).ready(function() {
  NProgress.start();
  initIsotope();
  ShowModal();
  initImage();
});