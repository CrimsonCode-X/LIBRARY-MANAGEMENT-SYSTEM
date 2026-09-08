type SearchResult = {
  title: string;
  authors: string[];
  cover_url?: string | null;
  sources: { provider: string; source_url?: string | null; reading_url?: string | null; access_type: string }[];
};

async function searchBooks(query: string): Promise<SearchResult[]> {
  const apiBase = process.env.API_BASE_URL ?? "http://localhost:8000";
  const response = await fetch(`${apiBase}/api/v1/search?q=${encodeURIComponent(query)}`, {
    cache: "no-store",
  });
  if (!response.ok) return [];
  const data = await response.json();
  return data.results ?? [];
}

export default async function SearchPage({ searchParams }: { searchParams: Promise<{ q?: string }> }) {
  const { q = "" } = await searchParams;
  const results = q ? await searchBooks(q) : [];

  return (
    <main>
      <h1>Search LibraryOS</h1>
      <form>
        <input name="q" defaultValue={q} placeholder="Search books..." />
        <button type="submit">Search</button>
      </form>
      <p>{q ? `${results.length} result(s)` : "Enter a search query."}</p>
      <ul>
        {results.map((book, index) => (
          <li key={`${book.title}-${index}`}>
            <h2>{book.title}</h2>
            <p>{book.authors.join(", ")}</p>
            <ul>
              {book.sources.map((source) => (
                <li key={`${source.provider}-${source.reading_url ?? source.source_url}`}>
                  {source.reading_url ? (
                    <a href={source.reading_url} target="_blank" rel="noreferrer">
                      {source.access_type === "UNKNOWN" ? "Open source" : source.access_type} — {source.provider}
                    </a>
                  ) : (
                    source.provider
                  )}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </main>
  );
}
