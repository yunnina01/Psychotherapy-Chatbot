// 시작하기 버튼 클릭 시
$('#btn_start').click(function() {
    $(this).hide();
    $('#caption').show();
    $('#popup_layer').show();
});

// 팝업 닫기 버튼 클릭 시
$('#popup_close').click(function() {
    $('#popup_layer').hide();
});

// 대화 시작 버튼 클릭 시
$('#btn_chat').click(function() {
    $(location).attr('href', '/chat');
});