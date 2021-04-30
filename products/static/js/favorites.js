$(document).ready(function(){

	$('span[name="fav"]').on('click', (event) => {

		let product_id = $(event.target).attr('id')
		let logo_class = $(event.target).attr('class')

		event.preventDefault();

		$.ajax({
			type: 'POST',
			url: '/products/favorites/',
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
				'product_id': product_id,

			},			
			success: function(response) {
				if (logo_class.indexOf('far') !== -1) {
					$(event.target).removeClass('far')
					$(event.target).addClass('fas')
				} else {
					$(event.target).removeClass('fas')
					$(event.target).addClass('far')			
				}
			},
		})


	})})
