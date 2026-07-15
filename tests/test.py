from woop import Scrap


page = Scrap("https://fr.wikipedia.org/wiki/Python_(langage)")

fichier = page.export_json(
    "quotes.json"
)

fichier_csv = page.export_csv("wiki.csv")

print("fichier cree : ", fichier_csv)


print(
    "Fichier créé :",
    fichier
)


print("Titre :")
print(page.title())


print("\nTexte :")
print(page.text())


print("\nLiens :")
print(page.links())


print("\nImages :")
print(page.images())

print("\nemails :")
print(page.emails())