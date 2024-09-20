function initProductSlider(sliderSelector, imgSelector) {
    var swiper = new Swiper(sliderSelector, {
        spaceBetween: 30,
        effect: 'fade',
        loop: false,
        navigation: {
            nextEl: '.next',
            prevEl: '.prev'
        },
        on: {
            init: function () {
                updateActiveImg(this);
            },
            slideChange: function () {
                updateActiveImg(this);
                updateNavigationButtons(this);
            }
        }
    });

    $(".js-fav").on("click", function () {
        $(this).find('.heart').toggleClass("is-active");
    });

    function updateActiveImg(swiperInstance) {
        var index = swiperInstance.activeIndex;
        var target = $(sliderSelector + '__item').eq(index).data('target');
        $(imgSelector + '__item').removeClass('active');
        $(imgSelector + '__item#' + target).addClass('active');
    }

    function updateNavigationButtons(swiperInstance) {
        if (swiperInstance.isEnd) {
            $('.prev').removeClass('disabled');
            $('.next').addClass('disabled');
        } else {
            $('.next').removeClass('disabled');
        }

        if (swiperInstance.isBeginning) {
            $('.prev').addClass('disabled');
        } else {
            $('.prev').removeClass('disabled');
        }
    }
}

// Initialize product sliders
initProductSlider('.product-slider', '.product-img');
initProductSlider('.rice-slider', '.rice-img');
initProductSlider('.chicken-slider', '.chicken-img');
initProductSlider('.veg-slider', '.veg-img');
initProductSlider('.bbq-slider', '.bbq-img');
initProductSlider('.pasta-slider', '.pasta-img');
initProductSlider('.roti-slider', '.roti-img');
initProductSlider('.roll-slider', '.roll-img');
initProductSlider('.chinese-slider', '.chinese-img');
initProductSlider('.durum-slider', '.durum-img');
initProductSlider('.soup-slider', '.soup-img');
initProductSlider('.sweet-slider', '.sweet-img');
initProductSlider('.drink-slider', '.drink-img');
initProductSlider('.addon-slider', '.addon-img');
// Add more items as needed...
