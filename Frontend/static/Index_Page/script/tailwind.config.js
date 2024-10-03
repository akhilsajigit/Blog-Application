tailwind.config = {
    theme: {
        extend: {
            gridTemplateColumns:{
                'auto': 'repeat(auto-fit,minmax(200px, 1fr))'
            },
            colors:{
                darkTheme: '#11001F'
            }
        }
    },
    darkMode: 'selector'
}