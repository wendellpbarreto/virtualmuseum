var carousel = $('#carousel');
var serverCarousel = $('.server__carousel');

/*
 *
 * Foundation
 * --------------------------------*/
 $(document).foundation({
    tab: {
      callback : function (tab) {
        var carousel = $('.server__carousel').data('owlCarousel');
        carousel._width = $('.server__carousel').width();
        carousel.invalidate('width');
        carousel.refresh();
      }
    }
  });

/*
 *
 * Document ready
 * --------------------------------*/
 $(document).ready(function(){

	// Carousels
    var postsCarouselCrop = $('.posts__carousel-crop');
	var postsCarouselCategory = $('.posts__carousel-category');
	var postsCarouselTitle = $('.posts__carousel-title');
	var photogalleryCarouselCrop = $('.photogallery__carousel-crop');
	var photogalleryCarouselTitle = $('.photogallery__carousel-title');

	carousel.owlCarousel({
		items: 1,
        lazyLoad: true,
        autoplay: true,
        loop: true,
        // animateOut: 'fadeOut',
        // animateIn: 'fadeIn',
    });
	$('.carousel__control-anchor.prev').click(function() {
		carousel.trigger('prev.owl.carousel');
	});
	$('.carousel__control-anchor.next').click(function() {
		carousel.trigger('next.owl.carousel');
	});



	$('#carousel').mouseenter(function() {
		$('.carousel__control-anchor.prev').removeClass('fadeOutLeft');
		$('.carousel__control-anchor.prev').addClass('fadeInLeft');
		$('.carousel__control-anchor.next').removeClass('fadeOutRight');
		$('.carousel__control-anchor.next').addClass('fadeInRight');
	}).mouseleave(function(){
		$('.carousel__control-anchor.prev').removeClass('fadeInLeft');
		$('.carousel__control-anchor.prev').addClass('fadeOutLeft');
		$('.carousel__control-anchor.next').removeClass('fadeInRight');
		$('.carousel__control-anchor.next').addClass('fadeOutRight');
	});

    serverCarousel.owlCarousel({
        items: 1,
        lazyLoad: true,
        autoplay: true,
        loop: true,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
    });


	// Tabs anchor
    var anchor = document.URL.indexOf("#");
    if (anchor != -1) {
        var hash = document.URL.substring(anchor + 1);
        $(".tabs").children("dd").each(function() {
            var id = $(this).find("a").attr("href").substring(1);
            var $container = $(".content#" + id);
            $(this).removeClass("active");
            $container.removeClass("active");
            if (id == hash) {
                $(this).addClass("active");
                $container.addClass("active");
                console.log($container)
            }
        });
    }
});

var engineSubmenu = function(anchor) {
    var navbarSubmenu = $('.navbar__submenu');
    var searchForm = $('.navbar__search');
    var searchFormInput = $('.navbar__search input');
    var searchFormButton = $('.navbar__search-button');
    var submenu;

    if (typeof anchor == 'undefined') {
        anchor = $('[data-submenu]');
        submenu = $('.submenu');
    } else {
        submenu = $('#' + anchor.attr('data-submenu'));
    }

    navbarSubmenu.stop();
    searchForm.stop();
    searchFormButton.stop();
    searchFormInput.stop();

    if (anchor.hasClass('active')) {
        anchor.removeClass('active');
        searchForm.removeClass('closed');

        navbarSubmenu.animate({ width: 3 }, 1500);
        searchForm.animate({ width: '40%' }, 1500);
        searchFormButton.animate({ width: '20%' }, 1500).queue(function(){
            searchFormInput.show();
            $(this).dequeue();
        }).queue(function(){
            submenu.hide();
            $(this).dequeue();
        });
    } else {
        anchor.addClass('active');
        searchForm.addClass('closed');

        searchFormInput.hide();
        searchFormButton.animate({ width: '100%' }, 1500);
        searchForm.animate({ width: '10%' }, 1500);
        navbarSubmenu.animate({ width: '88%' }, 1500);
        submenu.show();
    }
}

$(document).on('click', '[data-submenu]', function(ev) {
	ev.preventDefault();

    engineSubmenu($(this));
});

$(document).on('click', '.submenu__anchor', function(ev) {
    var anchor = document.URL.indexOf("#");
    if (anchor != -1) {
        var hash = document.URL.substring(anchor + 1);
        $(".tabs").children("dd").each(function() {
            var id = $(this).find("a").attr("href").substring(1);
            var $container = $(".content#" + id);
            $(this).removeClass("active");
            $container.removeClass("active");
            if (id == hash) {
                $(this).addClass("active");
                $container.addClass("active");
                console.log($container)
            }
        });
    }

    $('html, body').animate({
        scrollTop: $('body').offset().top
    }, 1);
});

$(document).on('submit', '.navbar__search.closed', function(ev){
    ev.preventDefault();

    engineSubmenu();
    $('#s').focus();

    return false;
})

$(document).on({
    mouseenter: function () {
        $(this).children('.servers__box').addClass('animated flipInX');
    },
    mouseleave: function () {
        $(this).children('.servers__box').removeClass('animated flipInX');
    }
}, '.servers__list-item');