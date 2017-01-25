harvest.pending = (function() {

    var
      configMap = {
        pending_model : null
      },

      stateMap = {},

      jqueryMap = {},

      loadPending, makePendingList,
      setJqueryMap, initModule;


    setJqueryMap = function() {
      var 
        $sources = $('.api-source');
        jqueryMap['sources'] = {};

      $.each($sources, function( i, source ) {
        var rabid = $( this ).data('rabid');
        var $panel = $( this ).find('.panel-collapse');

        jqueryMap.sources[rabid] = $panel;
      });
    };

    makePendingList = function( jsonList ) {
      var list_items = [];

      jsonList.forEach( function( pendingStr ) {
        var pendingObj = JSON.parse(pendingStr);
        var $li = $('<li/>', { 'class'       : 'list-group-item',
                            'data-source' : pendingObj.source,
                            'data-exid'   : pendingObj.exid,
                            });
        var $title = $('<span/>', {  'class' : 'pending-title',
                                  'text'  : pendingObj.title });
        var $venue = $('<span/>', {  'class' : 'pending-venue',
                                  'text'  : pendingObj.venue.abbrv });
        var $date = $('<span/>', { 'class' : 'pending-date',
                                'text'  : pendingObj.date.fulldate });
        $li.append($title);
        $li.append($venue);
        $li.append($date);

        list_items.push( $li );
      });

      return list_items;
    };

    loadPending = function (source) {
      var sourceData,
        $lis, $ul, $target;

        sourceData = configMap.pending_model.get_pending( source );
        $lis = makePendingList( sourceData );
        $ol = $('<ol/>', {'class' : 'list-group'});
        $lis.forEach( function($li) {
          $ol.append($li);
        });

        $target = jqueryMap.sources[ source ];
        $target.append($ol);     
    };

    configModule = function ( map ) {
      configMap.pending_model = map.pending_model;
    };

    initModule = function () {
      setJqueryMap();
    };

    return {
      loadPending: loadPending,
      configModule: configModule,
      initModule: initModule
    };
}());