harvest.pending = (function() {

    var
      configMap = {
        pending_model : null
      },

      stateMap = {},

      jqueryMap = {},

      loadPending, makePendingList,

      onClickPendingDetailsModal,
      setJqueryMap, initModule;


    setJqueryMap = function() {
      var 
        $sources = $('.api-source');
        jqueryMap = {
          'sources' : {},
          $modal : $('#modalDetails'),
          $table : $('#detailsTable'),
        };

      $.each($sources, function( i, source ) {
        var rabid = $( this ).data('rabid');
        var $panel = $( this ).find('.panel-collapse');

        jqueryMap.sources[rabid] = $panel;
      });
    };

    makePendingList = function( jsonList ) {
      var list_items = [];

      jsonList.forEach( function( pendingObj ) {
        var pendingObj,
            $li, $title, $venue, $date, $modal_btn;

        $li = $('<li/>', {  'class'       : 'list-group-item',
                            'data-source' : pendingObj.source,
                            'data-exid'   : pendingObj.exid,
                          });
        $title = $('<span/>', { 'class' : 'pending-title',
                                'text'  : pendingObj.title });
        $venue = $('<span/>', { 'class' : 'pending-venue',
                                'text'  : pendingObj.venue.abbrv });
        $date = $('<span/>', {  'class' : 'pending-date',
                                'text'  : pendingObj.date.fulldate });
        $modal_btn = $('<button/>', { 'type'        : 'button',
                                      'class'       : 'btn btn-primary details-modal',
                                      'data-exid'   : pendingObj.exid
                                    });

        $modal_btn.on('click', function(e) {
          e.preventDefault();

          var exid = $( this ).data('exid');
          onClickPendingDetailsModal( exid );
        });

        $li.append($title);
        $li.append($venue);
        $li.append($date);
        $li.append($modal_btn);

        list_items.push( $li );
      });

      return list_items;
    };

    loadPending = function (source) {
      var sourceData,
        $lis, $ul, $target;

        sourceData = configMap.pending_model.all( {'source' : source} );
        $lis = makePendingList( sourceData );
        $ol = $('<ol/>', {'class' : 'list-group'});
        $lis.forEach( function($li) {
          $ol.append($li);
        });

        $target = jqueryMap.sources[ source ];
        $target.append($ol);     
    };

    onClickPendingDetailsModal = function ( exid ) {
      var $modal, $table, details;
      
      $modal = jqueryMap.$modal;
      $table = jqueryMap.$table;
      $table.empty();

      details = configMap.pending_model.get( {'exid' : exid.toString() });
      for (var key in details) {
        if (details.hasOwnProperty(key)) {
          $tr = $('<tr/>');
          $key = $('<td/>', {'text' : key });
          $value = $('<td/>', {'text' : details[key]});

          $tr.append($key);
          $tr.append($value);
          $table.append($tr);
        }
      }
      $modal.modal('show');
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