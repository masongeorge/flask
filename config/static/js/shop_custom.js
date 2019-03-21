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

$(document).ready(function()
{
	initIsotope();
});