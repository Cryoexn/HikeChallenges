// Mountain
$(document).ready(function() {
    var mnt_progressbar = $('#progress_bar_mnt');
    mnt_max = mnt_progressbar.attr('max');
    mnt_time = (1000 / mnt_max) * 8;
    mnt_value = mnt_progressbar.val();
    mnt_current_pct = mnt_progressbar.val();

    var mnt_loading = function() {
        if (mnt_value == mnt_current_pct) {
            clearInterval(mnt_animate);
        } else {
            mnt_value += 1;
            mnt_progressbar.val(mnt_value);
        }

            $('#progress_bar_mnt').html(mnt_value + '%');
            var $mnt_ppc = $('.mnt-chart'),
            mnt_deg = 360 * mnt_value / 100;

            if (mnt_value > 50) {
                $mnt_ppc.addClass('gt-50');
            }

            $('#mnt-fill').css('transform', 'rotate(' + mnt_deg + 'deg)');
            $('#mnt-percents span').html(mnt_value + '%');
    };

     var mnt_animate = setInterval(function() { mnt_loading(); }, mnt_time);
});

// Elevation
$(document).ready(function() {
    var elv_progressbar = $('#progress_bar_elv');
    elv_max = elv_progressbar.attr('max');
    elv_time = (1000 / elv_max) * 6;
    elv_value = elv_progressbar.val();
    elv_current_pct = elv_progressbar.val();

    var elv_loading = function() {
        if (elv_value == elv_current_pct) {
            clearInterval(elv_animate);
        } else {
            elv_value += 1;
            elv_progressbar.val(elv_value);
        }

            $('#progress_bar_elv').html(elv_value + '%');
            var $elv_ppc = $('.elv-chart'),
            elv_deg = 360 * elv_value / 100;

            if (elv_value > 50) {
                $elv_ppc.addClass('gt-50');
            }

            $('#elv-fill').css('transform', 'rotate(' + elv_deg + 'deg)');
            $('#elv-percents span').html(elv_value + '%');
    };

     var elv_animate = setInterval(function() { elv_loading(); }, elv_time);
});

// Distance
$(document).ready(function() {
    var dist_progressbar = $('#progress_bar_dist');
    dist_max = dist_progressbar.attr('max');
    dist_time = (1000 / dist_max) * 4;
    dist_value = dist_progressbar.val();
    dist_current_pct = dist_progressbar.val();

    var dist_loading = function() {
        if (dist_value == dist_current_pct) {
            clearInterval(dist_animate);
        } else {
            dist_value += 1;
            dist_progressbar.val(dist_value);
        }

            $('#progress_bar_dist').html(dist_value + '%');
            var $dist_ppc = $('.dist-chart'),
            dist_deg = 360 * dist_value / 100;

            if (dist_value > 50) {
                $dist_ppc.addClass('gt-50');
            }

            $('#dist-fill').css('transform', 'rotate(' + dist_deg + 'deg)');
            $('#dist-percents span').html(dist_value + '%');
    };

     var dist_animate = setInterval(function() { dist_loading(); }, dist_time);
});