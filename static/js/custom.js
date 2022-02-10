'use strict';

(function($) {

    $(document).ready(function() {
        $('.set-bg').each(function() {
            var bg = $(this).data('setbg');
            $(this).css('background-image', 'url(' + bg + ')');

        });


        /*
	   Navbar
	*/
        var is_toggled = false
        $('.hamburger').on('click', function() {
            if (is_toggled == true) {
                $('.hamburger').removeClass('active');
                $('nav .menu').removeClass('active');
                is_toggled = false
            } else {
                $('.hamburger').addClass('active');
                $('nav .menu').addClass('active');
                is_toggled = true
            }
        })


        /* 
        Dashboard Sidebar
        */
        var is_sidebar_togggled = false

        $('#sidebarToggleTop').on('click', function() {
            if (is_sidebar_togggled == true) {
                $('.sidebar ,.dismiss, .overlay').removeClass('active');
                is_sidebar_togggled = false
            } else {
                $('.sidebar ,.dismiss, .overlay').addClass('active');

                is_sidebar_togggled = true
            }
        })
        $('#dismiss').on('click', function() {
            $('.sidebar ,.dismiss, .overlay').removeClass('active');
            is_sidebar_togggled = false
        })


        // When the user scrolls the page, execute myFunction
        if (document.getElementById("header") != null) {
            window.onscroll = function() { myFunction() };



            // Get the header
            var header = document.getElementById("header");

            // Get the offset position of the header
            var sticky = header.offsetTop;

        }
        // Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
        function myFunction() {
            if (window.pageYOffset >= sticky) {
                header.classList.add("sticky")
                $('.hero-section').addClass('top');
                $('.bg-half-170').addClass('top');
            } else {
                header.classList.remove("sticky");
                $('.hero-section').removeClass('top');
                $('.bg-half-170').removeClass('top');
            }
        }



        //testimony

        var silder = $(".owl-carousel");
        silder.owlCarousel({
            autoplay: true,
            autoplayTimeout: 3000,
            autoplayHoverPause: false,
            items: 1,
            stagePadding: 20,
            center: true,
            nav: false,
            margin: 50,
            dots: true,
            loop: true,
            responsive: {
                0: { items: 1 },
                480: { items: 1 },
                575: { items: 1 },
                768: { items: 1 },
                991: { items: 3 },
                1200: { items: 4 }
            }
        });



        /*
	    Wow
	*/
        new WOW().init();





    });
})(jQuery);