/**
 * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 * B U I L D   I N S T R U C T I O N S
 *
 * To build as PRODUCTION, either:
 *   -> Run "build-prod" or "prod" task; OR
 *   -> Run "gulp --production" in terminal
 *
 * To build as DEVELOPMENT, either:
 *   -> Run "build-dev" or "dev" task; OR
 *   -> Run "gulp --development" or "gulp" in terminal
 *
 * To WATCH for changes and build, either:
 *   -> Run "watch" task; OR
 *   -> Run "gulp --watch" in terminal
 *
 * To SPECIFY which app to watch or build:
 *   -> Run "gulp --<watch|production> --app=<NAME_OF_ROOT_FOLDER_IN_REACT_SRC>"; OR
 *   -> Run "gulp <watch|prod> --app=<NAME_OF_ROOT_FOLDER_IN_REACT_SRC>"
 *
 * To enable BROWSERSYNC:
 *   -> Run "gulp watch --proxy_host=<HOST:localhost> --proxy_port=<PORT:8080>; OR
 *   -> Run "gulp --watch --proxy_host=<HOST:localhost> --proxy_port=<PORT:8080>
 *   -> Open http://localhost:3000
 *
 * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 */

var gulp = require("gulp");
var gutil = require("gulp-util");
var gulpIf = require("gulp-if");
var eslint = require("gulp-eslint");
var uglify = require("gulp-uglify");
var rename = require("gulp-rename");
var notify = require("gulp-notify");
var glob = require("glob");
var nodeNotifier = require("node-notifier");
var plumber = require("gulp-plumber");
var browserify = require("browserify");
var watchify = require("watchify");
var babelify = require("babelify");
var cssModulesify = require("css-modulesify");
var sass = require("gulp-sass");
var livereactload = require("livereactload");
var browserSync = require("browser-sync").create();
var source = require("vinyl-source-stream");
var buffer = require("vinyl-buffer");
var es = require("event-stream");
var runSequence = require("run-sequence");
var moment = require("moment");


var flags = require("minimist")(process.argv.slice(2));
var isProduction = process.env.NODE_ENV === "production" || flags.production || flags.prod || false;
var shouldWatch = flags.watch || false;
var thisAppOnly = flags.app || null;

// BrowserSync proxy setup
var proxyHost = flags.proxy_host || "localhost";
var proxyPort = flags.proxy_port || 8080;

var isBuildSuccess = true;
var isWatching = false;


var ROOT = "frontend/";
var JS_ROOT = ROOT + "static/js/";
var CSS_ROOT = ROOT + "static/css/";
var REACT_ROOT = ROOT + "react_src/";
var HELPER_FILES = JS_ROOT + "helpers/**/*.js";
var REACT_FILES = REACT_ROOT + "**/*.+(js|jsx)";
var APP_ENTRY_FILES = REACT_ROOT + "*/index.js";
var BUNDLE_FILES = JS_ROOT + "/app/!(bundle.*.min).js";
var SCSS_ENTRY_FILES = REACT_ROOT + "**/scss/main.scss";


// Lint JS/JSX files
gulp.task("eslint", function () {
    return gulp.src([
        HELPER_FILES,
        REACT_FILES
    ])
        .pipe(eslint({
            useEslintrc: true
        }))
        .pipe(plumber())
        .pipe(eslint.format())
        .pipe(eslint.failAfterError())
        .on("error", notify.onError(function (error) {
            return {
                title: "<%= error.name %>",
                message: "<%= error.message %>"
            }
        }))
});


// Creates streams of each entry point
function createBundlers(useWatchify) {
    return glob.sync(APP_ENTRY_FILES).reduce(function (entries, entry, i) {
        var bundleName = entry.split("/")[2];

        if (thisAppOnly && thisAppOnly !== bundleName) {
            // check if specific app only is provided
            return entries;
        }

        return entries.concat(browserify({
            entries: entry,
            paths: [],
            debug: !isProduction,
            cache: {},  // required for watchify
            packageCache: {},  // required for watchify
            fullPaths: !isProduction,
        })
            .plugin(!isProduction && useWatchify ? livereactload : function () {}, {
                port: 4474 + i
            })
            .transform(babelify, {
                presets: ["es2015", "react", "stage-2"],
                env: {
                    development: {
                        plugins: [
                            ["react-transform", {
                                transforms: [{
                                    transform: "livereactload/babel-transform",
                                    imports: ["react"]
                                }],
                            }]
                        ]
                    }
                }
            })
            .plugin(cssModulesify, {
                output: CSS_ROOT + "bundle." + bundleName + ".css",
                after: "cssnano"
            }));
    }, []);
}


// Builds one bundler
function buildBundler(bundler, callback) {
    var bundleName = bundler._options.entries.split("/")[2];

    nodeNotifier.notify({
        title: "Gulp Build",
        message: "Building '" + bundleName + "' app...",
        time: 1000,
        "expire-time": 1000
    });

    return bundler
        .bundle()
        .on("error", notify.onError(function (error) {
            isBuildSuccess = false;
            return {
                title: "<%= error.name %>",
                message: "<%= error.message %>"
            }
        }))
        .on("error", function (error) {
            gutil.log(error.stack);
            this.emit("end");
        })
        .pipe(source(bundler._options.entries))
        .pipe(rename(function (path) {
            var dirnamesArray = path.dirname.split(process.platform === "win32" ? "\\" : "/");
            path.basename = "bundle." + dirnamesArray[dirnamesArray.length-1];
            path.dirname = "";
            path.extname = ".js";
        }))
        .pipe(buffer())
        .pipe(gulp.dest(JS_ROOT + "app"))
        .on("end", function () {
            callback && callback();
        });
}


// Compile React files using Browserify
function buildBundlers(bundlers, callback) {
    gulp.task("build", function () {
        var buildTasks = bundlers.map(function (bundler) {
            return buildBundler(bundler);
        });
        return es.merge(buildTasks);
    });

    nodeNotifier.notify({
        title: "Gulp Build",
        message: "Starting build for " + process.env.NODE_ENV + "...",
        time: 1000,
        "expire-time": 1000
    });

    isBuildSuccess = true;
    runSequence("sass", "build", "compress", function () {
        nodeNotifier.notify({
            title: "Gulp Build",
            message: isBuildSuccess ?
                ("Build for " + process.env.NODE_ENV + " successful!")
                :
                ("Build for " + process.env.NODE_ENV + " failed."),
            time: 1000,
            "expire-time": 1000
        });
    });

    return true;
}


// Preprocess SCSS to CSS
gulp.task("sass", function (callback) {
    var sassTasks = glob.sync(SCSS_ENTRY_FILES).map(function (entry) {
        var entryRootDir = entry.split("/").slice(0, -2).join("/");
        return gulp.src(entry)
            .pipe(sass())
            .on("error", notify.onError(function (error) {
                return {
                    title: "<%= error.name %>",
                    message: "<%= error.message %>"
                }
            }))
            .on("error", function (error) {
                gutil.log(error.stack);
                this.emit("end");
            })
            .pipe(rename({
                basename: "compiled",
                extname: ".css"
            }))
            .pipe(gulp.dest(entryRootDir))
    });
    es.merge(sassTasks)
        .on("end", callback);  // Signal DONE flag
});


// Compress the bundled file (only if production)
gulp.task("compress", function (callback) {
    if (isBuildSuccess) {
        var compressTasks = glob.sync(BUNDLE_FILES).reduce(function (entries, entry) {
            var bundleName = entry.split(".")[1];

            if (thisAppOnly && thisAppOnly !== bundleName) {
                // check if specific app only is provided
                return entries;
            }

            return entries.concat(gulp.src(entry)
                .pipe(gulpIf(isProduction, uglify()))
                .on("error", notify.onError(function (error) {
                    isBuildSuccess = false;
                    return {
                        title: "<%= error.name %>",
                        message: "<%= error.message %>"
                    }
                }))
                .on("error", function (error) {
                    gutil.log(error);
                    this.emit("end");
                })
                .pipe(rename({suffix: ".min"}))
                .pipe(gulp.dest(JS_ROOT + "app")));
        }, []);
        es.merge(compressTasks)
            .on("end", callback);  // Signal DONE flag
    }
    else {
        callback();
    }
});


// Watch for changes and bundle using Watchify
gulp.task("watch", ["sass"], function (callback) {
    process.env.NODE_ENV = "development";
    isWatching = true;

    var bundlingEnd = function (bundlingEndCallback) {
        runSequence("compress", function () {
            bundlingEndCallback && bundlingEndCallback();  // Signal DONE flag
            if (isBuildSuccess) {
                nodeNotifier.notify({
                    title: "Watch Build",
                    message: "Rebuild successful!",
                    time: 1000,
                    "expire-time": 1000
                });
            }
            gutil.log("-----------------------------------------------");
        });
    };

    var bundlers = createBundlers(true);
    var watchTasks = bundlers.map(function (bundler) {
        var watcher = watchify(bundler, {
            poll: true
        });
        watcher.on("update", function () {
            isBuildSuccess = true;
            buildBundler(watcher, bundlingEnd);
        });
        return buildBundler(watcher);
    });
    es.merge(watchTasks)
        .on("end", function () {
            bundlingEnd(callback);
        });

    browserSync.init({
        proxy: proxyHost + ":" + proxyPort,
        open: false,
        once: true,
        logFileChanges: false,
        logPrefix: moment().format('HH:mm:ss')
    });

    // Watch for changes in external CSS files
    gulp.task("watch-css", function () {
       return gulp.src(CSS_ROOT + "**/*.css")
           .pipe(browserSync.stream());
    });
    gulp.watch(CSS_ROOT + "**/*.css", ["watch-css"]);

    // Watch for changes in SCSS files
    gulp.watch(REACT_ROOT + "**/*.scss", ["sass"]);

    nodeNotifier.notify({
        title: "Watchify Started",
        message: "Open http://localhost:3000 to use BrowserSync.",
        time: 1000,
        "expire-time": 1000
    });
});


// Default task for DEVELOPMENT
var buildDev = function (callback) {
    process.env.NODE_ENV = "development";
    isProduction = false;
    buildBundlers(createBundlers(false), callback);
};
gulp.task("build-dev", buildDev);
gulp.task("dev", buildDev);


// Default task for PRODUCTION
var buildProd = function (callback) {
    process.env.NODE_ENV = "production";
    isProduction = true;
    buildBundlers(createBundlers(false), callback);
};
gulp.task("build-prod", buildProd);
gulp.task("prod", buildProd);


// Default entry
gulp.task("default", function (callback) {
    if (shouldWatch) {
        runSequence("build-dev", "watch", function () {
            callback();  // Signal DONE flag
        });
    }
    else {
        runSequence(isProduction ? "build-prod" : "build-dev", function () {
            callback();  // Signal DONE flag
        });
    }
});
