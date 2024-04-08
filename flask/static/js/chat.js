// 입력 버튼 클릭 시 동작
$('#btn_send').click(function() {
    $(this).attr('disabled', true)     // 2번 연속 사용자가 입력 못하도록 입력 버튼 비활성화
    send();
});
function send() {
    var userInput = $('#input').val();     // 사용자 입력 가져오기
    $('#divbox').append('<div class="msg_box send"><span>'+ userInput +'</span></div>');    // 사용자 메시지 표시
    $('#divbox').scrollTop($("#divbox")[0].scrollHeight);       // 스크롤 아래로 이동

    $.ajax({
        url: '/predict',        // Flask 라우트 경로로 변경
        type: 'POST',
        contentType: 'application/json',        // 데이터 타입 JSON으로 설정
        dataType: 'json',
        data: JSON.stringify({user_input: userInput}),      // JSON 문자열로 변환
        success: function(data) {
            $('#divbox').append('<div class="msg_box icon"><img src="../static/images/chatbot_icon.jpg" width="30" height="30"></div>');
            $('#divbox').append('<div class="msg_box receive"><span>'+ data.response +'</span></div>');     // 서버로부터 받은 응답 표시
            $("#divbox").scrollTop($("#divbox")[0].scrollHeight);       // 스크롤 아래로 이동
            $('#btn_send').attr('disabled', false)        // 입력 버튼 활성화
        },
        error: function(xhr, status, error) {
            $('#btn_send').attr('disabled', false)        // 입력 버튼 활성화
            console.error("Error: " + error);
            console.error("Status: " + status);
        }
    });
    $('#input').val('');       // 입력 필드 초기화
}

// 음성 버튼 클릭 시 동작
$('#btn_voice').click(function() {
    $(this).attr('disabled', true)      // 음성인식 중 음성 버튼 비활성화
    setTimeout(function() {             // 음성인식 팝업 지연 실행
        $('#popup_layer').show();
        $('#popup_voice').show();
    }, 400);
    voice();
});
function voice() {
    $.ajax({
        url: '/voice',
        type: 'POST',
        success: function(data) {
            $('#popup_layer').hide();
            $('#input').val(data.response);        // 입력란에 음성 인식 결과 출력
            $('#btn_voice').attr('disabled', false)     // 음성 버튼 활성화
        },
        error: function(xhr, status, error) {
            $('#popup_voice').hide();
            $('#popup_error').show();
            $('#btn_voice').attr('disabled', false)     // 음성 버튼 활성화
            console.error("Error: " + error);
            console.error("Status: " + status);
        }
    });
}

// 팝업 닫기 버튼 클릭 시
$('#popup_close').click(function() {
    $('#popup_error').hide();
    $('#popup_layer').hide();
});

/*
$('#form').on('submit', function(e) {
   e.preventDefault();
   send();
});
*/

/*
$('#close_chat_btn').on('click', function() {
    $('.chat_wrap').hide();
});
*/