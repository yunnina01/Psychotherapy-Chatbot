// 시작하기 버튼 클릭 시
$('#btn_start').click(function() {
    $(this).hide();                         // 시작하기 버튼 숨기기
    $('#btn_chat_box').show();              // 대화 시작 버튼 보이기
    $('#popup_layer').show();               // 주의사항 팝업 보이기
});

// 팝업 닫기 버튼 클릭 시
$('#popup_close').click(function() {
    $('#popup_layer').hide();               // 팝업창 숨기기
});

// 대화 시작 버튼 클릭 시
$('#btn_chat').click(function() {
    $(location).attr('href', '/chat');      // /chat으로 URL 이동
});