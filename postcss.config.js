module.exports = {
    plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
        // require('cssnano')({'preset': "advanced"}),
        require('@fullhuman/postcss-purgecss')({
            content: ['**/templates/*.html'],
            variables: true,
            keyframes: true,
            fontFace: true,
            defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || []
        })
    ]
}
