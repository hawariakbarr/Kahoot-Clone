// event pada saat link di klik

$('.page-scroll').on('click', function (e) {

	//ambil isi atribut href
	var tujuan = $(this).attr('href');

	//tangkap elemen
	var elemenTujuan = $(tujuan);

	$('html, body').animate({
		scrollTop: elemenTujuan.offset().top - 50

	}, 1300, 'easeInOutCubic');

	e.preventDefault();

});
//untuk paralax
//about
$(window).on('load', function () {
	$('.pKiri').addClass('pMuncul');
	$('.pKanan').addClass('pMuncul');
});
$(window).scroll(function () {

	var winScroll = $(this).scrollTop();

	//jumbotron
	$('.jumbotron img').css({
		'transform': 'translate(0px, ' + winScroll / 4 + '%)'

	});

	$('.jumbotron h1').css({
		'transform': 'translate(0px, ' + winScroll / 1.2 + '%)'

	});

	$('.jumbotron p').css({
		'transform': 'translate(0px, ' + winScroll / 0.83 + '%)'

	});

	//portfolio
	if (winScroll > $('.portfolio').offset().top - 360) {
		$('.portfolio .thumbnail').each(function (i) {
			setTimeout(function () {
				$('.portfolio .thumbnail').eq(i).addClass('muncul');

			}, 300 * i);
		});
	}
});

function newFunction() {
	console.log('.attr');
}