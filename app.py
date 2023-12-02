from flask import Flask, render_template, request, redirect, url_for
from store import Sklep

app = Flask(__name__)

sklep = Sklep()

@app.route('/', methods=['GET', 'POST'])
def index():
    sklep = Sklep()  # Create a new Sklep instance for each request
    saldo = sklep.konto()
    magazyn = sklep.get_magazyn()

    if request.method == 'POST':
        zmiana_saldo = request.form.get('zmiana_saldo')
        sklep.zmien_saldo(zmiana_saldo)
        sklep.zapisz_wszystko()

    return render_template('index.html', stan_konta=saldo, stan_magazynu=magazyn)



@app.route('/zakup', methods=['GET', 'POST'])
def formularz_zakupu():
    sklep = Sklep()
    if request.method == 'POST':
        nazwa_produktu = request.form['nazwa_produktu']
        cena = float(request.form['cena'])
        ilosc = int(request.form['ilosc'])
        sklep.zakup(nazwa_produktu, cena, ilosc)
        sklep.zapisz_wszystko()  # Save data after updating
        return redirect(url_for('index'))
    return render_template('zakup.html')

# Modify the 'formularz_sprzedazy' route
@app.route('/sprzedaz', methods=['POST'])
def formularz_sprzedazy():
    if request.method == 'POST':
        nazwa_produktu = request.form['nazwa_produktu']
        cena = float(request.form['cena'])
        ilosc = int(request.form['ilosc'])
        sklep.sprzedaz(nazwa_produktu, ilosc)  # Provide both 'nazwa_produktu' and 'ilosc'
        sklep.zapisz_wszystko()  # Save data after updating
        return redirect(url_for('index'))
    return render_template('sprzedaz.html')

@app.route('/historia/')
@app.route('/historia/<start>/<end>')
def history(start=None, end=None):
    all_history = sklep.get_history()  # Get all history entries

    try:
        if start is not None:
            start_index = int(start)
        else:
            start_index = 0

        if end is not None:
            end_index = int(end)
        else:
            end_index = len(all_history) - 1

        if start_index < 0 or end_index >= len(all_history) or start_index > end_index:
            raise ValueError(f"Zły zakres wybranej historii, ilość wpisów w naszej historii jest do: {len(all_history)}")

        selected_history = all_history[start_index:end_index + 1]
        return render_template('historia.html', history=selected_history, total_entries=len(all_history))

    except ValueError:
        return f"Zły zakres wybranej historii, ilość wpisów w naszej historii jest do: {len(all_history)}"


if __name__ == "__main__":
    app.run(debug=True)



