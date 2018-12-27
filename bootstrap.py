# iz modula random se uzima generator random broja uniformne raspodele
from random import uniform
import pygal


# Funkcija koja proverava unos i na osnovu argumenata vraca ceo ili realan broj (na osnovu floating buleanske promenljive)
# prompt ce prikazati poruku na ekranu pre nego sto ucita unos
def get_number(prompt = '', floating = False):
    if floating:
        while True:
            try:
                return float(input(prompt))
            except:
                print('Invalid input, try again.')
    else:
        while True:
            try:
                return int(input(prompt))
            except:
                print('Invalid input, try again.')


# Funkcija pomocu koje se unosi broj uzoraka koji ce se kreirati kao uzorci virtuelne populacije  (B)
def get_number_of_samples():
    print('\n/** The number should be bigger than 3000, if the number entered is lower or equal to 0, default will be used i.e. 3000 **/')
    number_of_samples = get_number('Enter the number of generated samples:')

    # Posto se generalno koristi B >= 3000, na neki nacin to forsiramo :D
    if number_of_samples <= 0:
        number_of_samples = 3000

    return number_of_samples


# Funkcija za unos duzine uzorka i uzorka, vraca iste
def get_sample():
    sample_dimension = get_number('Enter the length of sample:')

    # Vrsi se provera unosa
    while sample_dimension <= 0 :
        sample_dimension = get_number('The length should be a number bigger than 0.\n Please, try again:')

    # Unose se elementi uzorka, jedan po jedan
    print('Enter the sample, one at a time')
    sample = [get_number(floating = True) for _ in range(sample_dimension)]

    return sample_dimension, sample


# Funkcija za generisanje uzoraka i racunanje njihovih uzorackih sredina
def generate_and_get_mean(sample_dimension, sample = []):
    virtual_sample = []
    mean = 0

    # Pomocu petlje pravimo virtuelni uzorak koristeci random generator sa uniformnom raspodelom za generaciju random broja, moze se koristiti i neka druga (Normalna, gama, eksponencijalna i ostale raspodele)
    for i in range(0, sample_dimension):
        virtual_sample += [sample[int(uniform(0, sample_dimension))]]
        mean += float(virtual_sample[i])

    # Un-komentirati sledecu liniju za prikaz generisanog uzorka i njegove sredine uzoracke
    #print('mean:{}\t sample:{}'.format(round((mean / float(sample_dimension)), 5), str(virtual_sample)))

    # Rezultat se zaokruzuje na pet decimala iz estetskih razloga
    return round(mean / sample_dimension, 5)


# Unos intervala poverenja, provera unosa i vraca se broj iz segmenta [0,1] zarad laksih daljih proracuna
def get_confidence_interval():
    confidence_interval = get_number('\nConfidence interval is percentile and should be between 0 and 100\nEnter the confidence interval:', floating = True)

    while confidence_interval > 100 or confidence_interval <= 0:
        confidence_interval = get_number('Percents should be between 0 and 100', floating = True)

    return confidence_interval / 100


# Main funkcija
def main():
    mean_array = []
    print('Welcome to BOOTSTRAP confidence interval program by Hamza and Anes!\n')

    # Unos obima uzorka, uzorka, broj generisanih uzoraka i intervala poverenja
    sample_dimension, sample = get_sample()
    number_of_samples = get_number_of_samples()
    confidence_interval = get_confidence_interval()

    # Procenat niza koji treba odstraniti na osnovu intervala poverenja
    removal_percent = (1 - confidence_interval ) / 2

    # Generise se number_of_samples uzoraka i racunaju se njihove uzoracke sredine, koje se smestaju u jedan niz duzine od 0 do number_of_samples - 1
    for i in range(0, number_of_samples):
        mean_array += [generate_and_get_mean(sample_dimension, sample)]

    # Sortira se niz uzorackih sredina virtuelno generisanih uzoraka
    mean_array.sort()

    # Donja granica je element koji se nalazi na removal_percent - 1 mestu u nizu, dok je gornja granica na confidence_interval - removal_percent - 1 mestu u nizu
    lower_bound = mean_array[int(number_of_samples * removal_percent) - 1]
    upper_bound = mean_array[int(number_of_samples * (confidence_interval - removal_percent)) - 1]

    lower_index = mean_array.index(lower_bound)
    upper_index = mean_array.index(upper_bound)

    # Graficki prikaz rezultata
    line_chart = pygal.XY(xrange=(0, number_of_samples))

    # Linije 1 i 3 cine elementi koji su van intervala
    # Liniju 2 cine elementi unuter intervala
    line1 = list(zip(range(lower_index), mean_array[:lower_index]))
    line2 = list(zip(range(lower_index, upper_index), mean_array[lower_index:upper_index]))
    line3 = list(zip(range(upper_index, number_of_samples), mean_array[upper_index:]))

    line_chart.add('Van intervala poverenja', line1)
    line_chart.add('U intervalu poverenja', line2)
    line_chart.add('Van intervala poverenja', line3)

    # Dobijeni graficki prikaz je sacuvan kao vektorska slika
    # s nazivom 'bootstrap.svg'. Otvoriti je u browseru.
    line_chart.render_to_file('bootstrap.svg')
    #  Automatski se rezultat prikazuje graficki u browseru
    line_chart.render_in_browser()

    print('\n\nLOWER BOUND IS:' + str(lower_bound) + '\nUPPER BOUND IS:' + str(upper_bound))
    print('\n\n\n=== GOODBYE! === ')


# Pokretanje programa :)
if __name__ == "__main__":
    main()