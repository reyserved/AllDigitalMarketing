$.noConflict();

jQuery(document).ready(function() {

    var owl;






    jQuery('#carousel-custom-dots').on('click', 'li', function(e) {

        jQuery('#carousel-custom-dots .owl-dot').removeClass('active');

        jQuery(this).addClass("active");

        owl.trigger('to.owl.carousel', [jQuery(this).index(), 300]);

    });



    jQuery('.custom-next').click(function() {

        owl.trigger('next.owl.carousel');

    });

    jQuery('.custom-prev').click(function() {

        owl.trigger('prev.owl.carousel', [300]);

    });



    jQuery("#fun-facts").owlCarousel({

        autoplay: true,

        autoplayHoverPause: false,

        autoplayTimeout: 7000,

        loop: true,

        items: 3,

        margin: 0,

        dots: false,

        mouseDrag: true,

        nav: true,

        navText: ['<i class="fas fa-arrow-left"></i>', '<i class="fas fa-arrow-right"></i>'],

        responsiveClass: true,

        responsive: {

            0: {

                items: 1,

                margin: 10,

            },

            640: {

                items: 2,

                margin: 20,

            },

            768: {

                items: 2,

                margin: 30,

            },

            1024: {

                items: 3,

                margin: 30,

            }

        }

    });



    jQuery("#divorce-mediator").owlCarousel({

        autoplay: true,

        autoplayHoverPause: false,

        autoplayTimeout: 7000,

        loop: true,

        items: 1,

        margin: 0,

        dots: false,

        mouseDrag: true,

        nav: true,

        navText: ['<img src="' + siteurl + '/assets/images/prev.png" alt="prev">', '<img src="' + siteurl + '/assets/images/next.png" alt="prev">'],

        responsiveClass: true,

        responsive: {

            0: {

                nav: true,

            },

            480: {

                nav: true,

            },

            980: {

                nav: true,

            }

        }





    });



    var owl2;

    owl2 = jQuery("#testi-slider").owlCarousel({

        autoplay: false,

        autoplayHoverPause: false,

        autoplayTimeout: 7000,

        loop: true,

        items: 1,

        margin: 0,

        dots: true,

        mouseDrag: true,

        nav: false,

        navText: ['<i class="fas fa-chevron-left"></i>', '<i class="fas fa-chevron-right"></i>'],

        responsiveClass: true,

        dotsContainer: '#carousel-custom-dots2',

    });



    jQuery('#carousel-custom-dots2').on('click', 'li', function(e) {

        jQuery('#carousel-custom-dots2 .owl-dot').removeClass('active');

        jQuery(this).addClass("active");

        owl2.trigger('to.owl.carousel', [jQuery(this).index(), 300]);

    });



    jQuery('.custom-next2').click(function() {

        owl2.trigger('next.owl.carousel');

    });

    jQuery('.custom-prev2').click(function() {

        owl2.trigger('prev.owl.carousel', [300]);

    });



    jQuery("#step-accordion").bwlAccordion();



    jQuery(".faq-acc-cont").bwlAccordion({

        closeall: true

    });


    jQuery('.tab-wrapper').easytabs({
        updateHash: false,
    });


    var jQuerymenu = jQuery('.nav-menu');



    jQuerymenu.smartmenus({

        subMenusSubOffsetX: 2,

        subMenusSubOffsetY: 0,

        subMenusMinWidth: '200px'

    });





    menuRight = document.getElementById('cbp-spmenu-s2'),

        showRightPush = document.getElementById('showRightPush'),

        closePush = document.getElementById('closePush'),

        body = document.body;





    showRightPush.onclick = function() {

        classie.toggle(this, 'active');

        classie.toggle(body, 'cbp-spmenu-push-toleft');

        classie.toggle(menuRight, 'cbp-spmenu-open');

    };

    closePush.onclick = function() {

        classie.toggle(this, 'active');

        classie.toggle(body, 'cbp-spmenu-push-toleft');

        classie.toggle(menuRight, 'cbp-spmenu-open');

    };

    jQuery('header.site-header').scrollToFixed();




    var jQueryheader = jQuery('.site-header'),

        scrollClass = 'sticky-header',

        activateAtY = 10;



    function deactivateHeader() {

        if (!jQueryheader.hasClass(scrollClass)) {

            jQueryheader.addClass(scrollClass);

        }

    }



    function activateHeader() {

        if (jQueryheader.hasClass(scrollClass)) {

            jQueryheader.removeClass(scrollClass);

        }

    }



    jQuery(window).scroll(function() {

        if (jQuery(window).scrollTop() > activateAtY) {

            deactivateHeader();

        } else {

            activateHeader();

        }

    });



    new WOW().init();



});