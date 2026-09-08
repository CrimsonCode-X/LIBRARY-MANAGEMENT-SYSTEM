export default function HomePage() {
  return (
    <main>
      <section>
        <p>LibraryOS</p>
        <h1>Discover books across digital libraries.</h1>
        <p>
          Search a unified catalogue and find legitimate ways to read or access books online.
        </p>
        <form action="/search">
          <label htmlFor="q">Search books</label>
          <input id="q" name="q" placeholder="Title, author, ISBN..." required />
          <button type="submit">Search</button>
        </form>
      </section>
    </main>
  );
}
