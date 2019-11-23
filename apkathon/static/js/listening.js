const APIkey = 'AIzaSyB86ekaFz7Gdkz0nIWElw8JShe_FZlhKOA';
const URL = 'https://www.googleapis.com/youtube/v3/playlistItems';
const URLSearch = 'https://www.googleapis.com/youtube/v3/search';

const channelNames = ['TED', 'BBC', 'CNN', 'TheEllenShow', 'Motivation2Study', 'VOA Learning English', 'Learn English With TV Series'];
const channelIDs = ['UUAuUUnT6oDeKwE6v1NGQxug', 'UUCj956IF62FbT7Gouszaj9w', 'UUupvZG-5ko_eiXAupbDfxWw', 'UUp0hYYBW6IMayGgR-WeoCvQ', 'UU8PICQUP0a_HsrA9S4IIgWw', 'UUKyTokYo0nK2OA-az-sDijA', 'UUKgpamMlm872zkGDcBJHYDg'];

const chanIds = ['UCAuUUnT6oDeKwE6v1NGQxug', 'UC16niRr50-MSBwiO3YDb3RA', 'UCupvZG-5ko_eiXAupbDfxWw', 'UCp0hYYBW6IMayGgR-WeoCvQ', 'UC8PICQUP0a_HsrA9S4IIgWw', 'UCKyTokYo0nK2OA-az-sDijA', 'UCKgpamMlm872zkGDcBJHYDg'];

var options = {
    part: 'snippet',
    key: APIkey,
    maxResults: 3,
    q: '',
    playlistId: channelIDs[0],
    channelId: ''
}



$(document).ready(function() {

    loadVids(URL, channelIDs, options);

    function loadVids(URL, channelIDs, options) {

        for (let i = 0; i < channelIDs.length; i++) {
            options.playlistId = channelIDs[i];
            //console.log(options.playlistId)
            $.getJSON(URL, options, function(data) {
                //var id = data.items[0].snippet.resourceId.videoId;
                //mainVid(id);
                resultsLoop(data, i + 1);
            });
        }

    }



    function mainVid(id) {
        $('#video-learning').html(`
               <p> <iframe id="${id}" src="https://www.youtube.com/embed/${id}?enablejsapi=1" width="500" height="315" allowfullscreen="allowfullscreen"></iframe></p>
                    <div id="videoTranscript${id}" class="mmocVideoTranscript" data-language="no" data-name="bokm&aring;l"></div>
                `);

        $.getScript("https://pfdk.github.io/frontend/youtube.js");

        return true;
    }


    function transcriptVid(id) {
        $('#video-transcipt').html(`
        <div id="videoTranscript${id}" class="mmocVideoTranscript" data-language="no" data-name="bokm&aring;l"></div>
    `);
    }

    function resultsLoop(data, catNum) {
        // $('div.row.showVideos').empty();
        const $showList = 'div.row.showVideos-' + catNum;
        $($showList).empty();
        $.each(data.items, function(i, item) {

            var thumb = item.snippet.thumbnails.medium.url;
            var title = item.snippet.title;
            var channelTitle = item.snippet.channelTitle;

            var vid = item.snippet.resourceId.videoId;

            $($showList).append(`
                <div class="col-xl-4 col-lg-4 col-md-6" data-key="${vid}">
                    <div class="single_courses">
                        <div class="thumb">
                            <a href="#area-to-scroll">
                                <img src="${thumb}" alt="">
                            </a>
                        </div>
                        <div class="courses_info">
                            <span>${channelTitle}</span>
                            <h3><a href="#area-to-scroll">${title}</a></h3>
                        </div>
                    </div>
                </div>
            `);
        });
    }

    // CLICK EVENT
    $('div.tab-content#myContent').on('click', 'div.col-xl-4.col-lg-4.col-md-6', function() {
        $('#close-video-learning').show();
        $('div.listening-area.container.p-3').show();
        var id = $(this).attr('data-key');
        mainVid(id);

        //transcriptVid(id);
    });
    $('#close-video-learning').on('click', function() {
        $('div.listening-area.container.p-3').hide();
    });

});

function loadVidsbyTopic(chanIds, options, q) {
    options.q = q;
    options.playlistId = '';
    for (let i = 0; i < channelIDs.length; i++) {
        options.channelId = chanIds[i];
        //console.log(options.playlistId)
        $.getJSON(URLSearch, options, function(data) {
            resultsLoopbyTopic(data, i + 1);
        });
    }

}

function resultsLoopbyTopic(data, catNum) {
    // $('div.row.showVideos').empty();
    const $showList = 'div.row.showVideos-' + catNum;
    $($showList).empty();
    $.each(data.items, function(i, item) {

        var thumb = item.snippet.thumbnails.medium.url;
        var title = item.snippet.title;
        var channelTitle = item.snippet.channelTitle;

        var vid = item.id.videoId;

        $($showList).append(`
            <div class="col-xl-4 col-lg-4 col-md-6" data-key="${vid}">
                <div class="single_courses">
                    <div class="thumb">
                        <a href="#area-to-scroll">
                            <img src="${thumb}" alt="">
                        </a>
                    </div>
                    <div class="courses_info">
                        <span>${channelTitle}</span>
                        <h3><a href="#area-to-scroll">${title}</a></h3>
                    </div>
                </div>
            </div>
        `);
    });
}
